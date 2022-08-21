import FlexibleNetwork.Vendors as supported_vendors
from FlexibleNetwork.Flexible_Network import ReadCliOptions
from FlexibleNetwork.Flexible_Network import CLI
from FlexibleNetwork.Flexible_Network import Config
from FlexibleNetwork.Flexible_Network import Inventory
from FlexibleNetwork.Flexible_Network import SSH_Authentication
from FlexibleNetwork.Integrations import RocketChat_API
from FlexibleNetwork.Integrations import S3_APIs
from FlexibleNetwork.Integrations import Cyberark_APIs_v2
from FlexibleNetwork.yaml_parser import YamlParser
from tabulate import tabulate
import uuid
from FlexibleNetwork.Flexible_Network import TinyDB_db
from FlexibleNetwork.Flexible_Network import Bcolors
import json
from pygments import highlight, lexers, formatters
from datetime import datetime
from pathlib import Path
import time
import os
import textwrap
import rich
from rich.markdown import Markdown
# from rich.panel import Panel
# from rich.console import Console
from rich.table import Table
from rich.console import Console, Group
from rich.rule import Rule
from tinydb import Query


class Terminal_Task(SSH_Authentication):

    task_name = None # Should be updated from a cli option. --name

    def __init__(self, task_name="", task_log_format='markdown'):
        super().__init__(debug=ReadCliOptions.debug)

        self.bcolors = Bcolors()
        
        self.yaml_file = None
        self.task_name = task_name
        self.task_log_format = task_log_format
        self.hosts_connected_total_number = 0
        # Check task_log_format
        if self.task_log_format not in ['txt', 'markdown']:
            print(f"ERROR -- unsupported log format '{self.task_log_format}' , supported: {['txt', 'markdown']}")
            exit(1)

        # Initialize the "CLI" class so that it read the cli options 
        cli = CLI()
        cli.argparse()

        # Initialize the DB because we'll need it if '--task list' or '--backup list' are specified
        self.db = TinyDB_db()

        # Read the "debug" flag from cli 
        self.debug = ReadCliOptions.debug

        # List tasks (--task)
        if ReadCliOptions.list_tasks:
            print(self.list_all_tasks(all=ReadCliOptions.list_all))
            exit(0)

        # List backups (--backup)
        if ReadCliOptions.list_backups:
            print(self.list_all_backups(all=ReadCliOptions.list_all))
            exit(0)

        if ReadCliOptions.delete_backup:
            self.delete_config_backup(backup_id=ReadCliOptions.delete)

        if ReadCliOptions.delete_task:
            self.delete_task(task_id=ReadCliOptions.delete)

        if ReadCliOptions.get_log:
            print(self.db.get_task_log(ReadCliOptions.get_log))

        if ReadCliOptions.get_backup:
            # Get the backup with the backup-id
            result = self.db.return_backup(ReadCliOptions.get_backup)
            if result.exit_code == 0:
                print(result.text)
                exit(0)
            else:
                print(f"ERROR -- {result.stderr}")
                print(self.bcolors.FAIL + result.text + self.bcolors.ENDC)
                exit(1)

        # Initialize the "Config" class so that it checks the config file at the begining. 
        config = Config()
        # Need to organize
        self.validate_integrations()
        self.inventory = Inventory()
        self.vendor = supported_vendors.Cisco() # Default vendor class should exist in the config
        # self.ssh = SSH_connection()
        # self.ssh.vendor = self.vendor

        
        self.local_db_dir = self.db.local_db_dir
        self.log_and_backup_dir = self.local_db_dir +  '/' + datetime.today().strftime('%Y') + '/' + datetime.today().strftime('%m') + '/' + datetime.today().strftime('%d')
        # Create the dir if doesn't exist
        if not os.path.isdir(self.log_and_backup_dir):
            Path(self.log_and_backup_dir).mkdir(parents=True, exist_ok=True)
        # Gernate the task id
        self.task_id = str(uuid.uuid4())
        self.log_file = self.log_and_backup_dir + '/' + self.task_id + '.txt'
        
        # By default do NOT log the output,
        # this will be set to True if number_of_authenticated_devices > 0
        self.log_output = False
        self.log_output_file = None
        # create a row in the tasks table & add the id & name
        date = datetime.today().strftime('%d-%m-%Y')
        time = datetime.today().strftime('%H:%M:%S')

        ### Get the task name ###
        # If task name is provided via CLI
        if ReadCliOptions.task_name is not None:
            self.task_name = str(ReadCliOptions.task_name)

        # If task name is NOT provided (via CLI or at Class initialization)
        if ReadCliOptions.yaml_file is None:
            if not self.task_name:
                rich.print("[bold]ERROR -- The task name must be provided\n")
                cli.parser.print_help()
                exit(1)

        # Insert an entry in the DB for the Task
        self.db.insert_tasks_table({'id': self.task_id, 
                                   'name': self.task_name,
                                   'format': self.task_log_format,
                                   'n_of_backups': 0, 
                                   'backups_ids': [],
                                   'log_file': None,
                                   'date': date, 
                                   'time': time,
                                   'n_of_hosts': 0,
                                   'n_of_connected_hosts': 0
                                   })

        # Read all inventory sections
        # self.inventory = self.inventory.read_inventory()
        self.inventory_groups = self.inventory.read_inventory()
        self.inventory_groups_names = []
        for i in self.inventory_groups.keys():
            self.inventory_groups_names.append(i)

        self.group_to_authenticate_from_cli = ReadCliOptions.authenticate_group

        # Check YAML file input
        if ReadCliOptions.yaml_file is not None:
            self.yaml_file = ReadCliOptions.yaml_file
            if not os.path.exists(self.yaml_file):
                print(f"ERROR -- File '{self.yaml_file}' does NOT exist")
                exit(1)
            if not os.path.isfile(self.yaml_file):
                print(f"ERROR -- File '{self.yaml_file}' is NOT a file")
                exit(1)
            
            # Check the YAML file extension
            filename, file_extension = os.path.splitext(self.yaml_file)
            if file_extension not in ['.yaml', '.yml']:
                print("ERROR -- Invalid file extension .. supported extensions are .yaml AND .yml ")
                exit(1)

            # Parse the YAML file
            yamlParser = YamlParser(self.yaml_file)

            # Validate the YAML file and print a message
            if ReadCliOptions.yaml_file_check:
                # With print_msg=True, it will only validate and exit
                yamlParser.validate_yaml(print_msg=True)

            # Validate the YAML file and parse it
            validated_docs = yamlParser.validate_yaml()
            for doc in validated_docs:
                self.task_name = doc.get('Task').get('name')
                self.task_log_format = doc.get('Task').get('log_format')
                # Update the DB (task name & log format)
                self.db.update_tasks_table(task_id=self.task_id, 
                                           dct={
                                            'name': self.task_name,
                                            'format': self.task_log_format
                                            })
                # Setting the choosen vendor
                if doc.get('Task').get('vendor') == 'cisco':
                    self.vendor = supported_vendors.Cisco
                elif doc.get('Task').get('vendor') == 'huawei':
                    self.vendor = supported_vendors.Huawei
                # Run each sub-task
                for subtask in doc.get('Task').get('subTask'):
                    password = None
                    privileged_mode_password = None
                    username = None

                    # Getting password
                    if subtask.get('authenticate').get('password').get('value'):
                        password = subtask.get('authenticate').get('password').get('value')
                    elif subtask.get('authenticate').get('password').get('value_from_env').get('key'):
                        # Reading password from ENV
                        password = self.read_env_key(subtask.get('authenticate').get('password').get('value_from_env').get('key'))
                    else:
                        print("ERROR -- can NOT find 'password' !")
                        exit(1)
                
                    # Getting privileged_mode_password
                    if subtask.get('authenticate').get('privileged_mode_password').get('value'):
                        privileged_mode_password = subtask.get('authenticate').get('privileged_mode_password').get('value')
                    elif subtask.get('authenticate').get('privileged_mode_password').get('value_from_env').get('key'):
                        # Reading password from ENV
                        privileged_mode_password = self.read_env_key(subtask.get('authenticate').get('privileged_mode_password').get('value_from_env').get('key'))
                    else:
                        print("ERROR -- can NOT find 'privileged_mode_password' !")
                        exit(1)

                    # Getting username
                    if subtask.get('authenticate').get('username').get('value'):
                        username = subtask.get('authenticate').get('username').get('value')
                    elif subtask.get('authenticate').get('username').get('value_from_env').get('key'):
                        # Reading username from ENV
                        username = self.read_env_key(subtask.get('authenticate').get('username').get('value_from_env').get('key'))
                    else:
                        print("ERROR -- can NOT find 'username' !")
                        exit(1)

                    # Run it
                    self.sub_task(name=subtask.get('name'),
                                  group=subtask.get('authenticate').get('group'),
                                  username=username,
                                  password=password,
                                  privileged_mode_password=privileged_mode_password,
                                  port=subtask.get('authenticate').get('port'),
                                  cmds=subtask.get('commands'),
                                  reconnect=subtask.get('authenticate').get('reconnect'),
                                  take_config_backup_dct=subtask.get('configBackup'))
            
            # Exit after running the Yaml manifest
            exit(0)

        if ReadCliOptions.authenticate_group:
            # Get the IPs of the section to the 'self.inventory' attribute
            # self.inventory = self.inventory.get_section(self.group_to_authenticate_from_cli)
            # If the section not found the 'get_section' method will return None
            # Hence the script will exit with code 1
            # if self.inventory is None:
            #     print("\nERROR -- Inventory section [ {} ] does NOT exist !".format(ReadCliOptions.authenticate_group))
            #     exit(1)
            # # Stop if the choosen group is empty
            # if not self.inventory:
            #     print("\n> The choosen group [ {} ] has no hosts .. No need to continue.".format(ReadCliOptions.authenticate_group))
            #     exit(0)
            # Read the user, password, port 
            self.user = ReadCliOptions.auth_user
            self.password = ReadCliOptions.auth_password
            # Default port is 22 if not specified in the CLI
            self.port = ReadCliOptions.auth_port
            # Authenticate the choosen group
            self.authenticate(groups=self.group_to_authenticate_from_cli, user=self.user, password=self.password, port=self.port)
            
    def validate_integrations(self):
        if ReadCliOptions.to_validate_lst is not None:
            """
            Validate RocketChat Authentication.
            """
            print("\n> Validating Integration")
            table = [['Integration', 'Status', 'Comment']]
            tabulate.WIDE_CHARS_MODE = False

            all_good = True 
            if 'rocketChat' in ReadCliOptions.to_validate_lst:
                rocket = RocketChat_API() 
                auth = rocket.auth_raw()
                out = { 'success': False, 'comment': ""}
                if auth['success']:
                    out['success'] = True
                    out['comment'] = "Works !"
                else:
                    out['comment'] = auth['fail_reason']

                if out['success']:
                    status = '🟢'
                else:
                    status = '🔴'
                    all_good = False
                comment = "\n".join(textwrap.wrap(out['comment'], width=50, replace_whitespace=False))
                row = ['rocketChat', status, comment]
                table.append(row)
            if 's3' in ReadCliOptions.to_validate_lst:
                s3 = S3_APIs()
                auth = s3.authenticate_raw()
                out = { 'success': False, 'comment': ""}
                if auth['success']:
                    out['success'] = True
                    out['comment'] = "Works !"
                else:
                    out['comment'] = auth['fail_reason']

                if out['success']:
                    status = '🟢'
                else:
                    status = '🔴'
                    all_good = False
                comment = "\n".join(textwrap.wrap(out['comment'], width=50, replace_whitespace=False))
                row = ['S3', status, comment]
                table.append(row)
            if 'cyberArk' in ReadCliOptions.to_validate_lst:
                cyberark = Cyberark_APIs_v2()
                auth = cyberark.authenticate_raw()
                out = { 'success': False, 'comment': ""}
                if auth['success']:
                    out['success'] = True
                    out['comment'] = "Works !"
                else:
                    out['comment'] = auth['fail_reason']
                if out['success']:
                    status = '🟢'
                else:
                    status = '🔴'
                    all_good = False
                comment = "\n".join(textwrap.wrap(out['comment'], width=50, replace_whitespace=False))
                row = ['cyberArk', status, comment]
                table.append(row)
            out = tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)
            print(out)
            if all_good:
                exit(0)
            else:
                exit(1)

    def authenticate(self, groups, user, password, privileged_mode_password="", port=22, terminal_print=True):
        """
        Authenticate an inventory groups
        INPUT:
            1. groups (list) List of inventory groups
            2. user (string)
            3. password (string)
            4. port (int) [Default: 22]
            5. terminal_print (bool) [Default: True] whether to print the progress to the terminal

        Under optimization
        """
        class Output:
            def __init__(self):
                self.connection_report_table = ""
                self.hosts_total = [] 
                self.hosts_connected = []
                self.hosts_failed =  []
                self.hosts_total_number = 0
                self.hosts_connected_number = 0
                self.hosts_failed_number = 0
        output = Output()

        # If only 1 group was provided as a string, convert it to a list
        if not isinstance(groups, list):
            groups = [groups]

        # Check if the provided groups exists in the inventory
        for group in groups:
            if group not in self.inventory_groups_names:
                rich.print(f"INFO -- Group [ [bold]{group}[/bold] ] does in exist in the inventory file, available sections:\n{self.inventory_groups_names}")
                exit(1)

        # Check if the group is empty
        for group in groups:
            group_hosts =  self.inventory.get_section(group)
            if not group_hosts:
                rich.print(f"INFO -- Group [ [bold]{group}[/bold] ] has no hosts .. No need to continue.")
                exit(0) 

        output.hosts_total = []
        output.hosts_connected = []
        output.hosts_failed = []
        # Getting the hosts of all groups, and then authenticate them at once
        for group in groups:
            # Getting the hosts of the group (dct)
            group_hosts = self.inventory.get_section(group)
            # Concatenate the group hosts to output.hosts_total
            output.hosts_total = output.hosts_total + list(group_hosts.keys())

        # Authenticate group
        # => The output is a dct of 2 dcts, one is "hosts" (contains dct for each host, where the ip is the key and the value is the information) ad another "total" (general information about the hosts)
        auth = self.authenticate_hosts(hosts=output.hosts_total, group_name=group, user=user, password=password, privileged_mode_password=privileged_mode_password, port=port, terminal_print=terminal_print, debug=self.debug)

        if len(auth.get('hosts')) >= 1:
            for host_ip, host_info in auth.get('hosts').items():
                if host_info['is_connected']:
                    output.hosts_connected.append(host_ip)
                else:
                    output.hosts_failed.append(host_ip)

        
        output.hosts_total_number = auth.get('total').get('n_hosts_total')
        output.hosts_connected_number = auth.get('total').get('n_hosts_connected')
        output.hosts_failed_number = auth.get('total').get('n_hosts_failed')
        output.connection_report_table = self.connection_report_Table(dct=auth.get('hosts'), terminal_print=False, ask_when_hosts_fail=False)

        self.db.update_tasks_table(
            task_id=self.task_id,
            dct={
            'n_of_hosts': output.hosts_total_number,
            'n_of_connected_hosts': output.hosts_connected_number
            })

        # Update the connected devices number
        self.hosts_connected_total_number += output.hosts_connected_number

        self.db.update_tasks_table({'full_devices_n': output.hosts_total_number}, self.task_id)
        self.db.update_tasks_table({'authenticated_devices_n': output.hosts_connected_number}, self.task_id)
        if terminal_print:
            if ReadCliOptions.no_confirm_auth:
                ask_when_hosts_fail_ = False
            else:
                ask_when_hosts_fail_ = True
            self.connection_report_Table(dct=auth.get('hosts'), terminal_print=True, ask_when_hosts_fail=ask_when_hosts_fail_)
        # If connected_devices_number > 0 , set the log_output flag to True
        if self.hosts_connected_total_number > 0:
            self.log_output = True
            # if not os.path.isdir(self.log_and_backup_dir):
            #     Path(self.log_and_backup_dir).mkdir(parents=True, exist_ok=True)
            self.db.update_tasks_table({'log_file': self.log_file}, self.task_id)
        else:
            self.db.update_tasks_table({'log_file': None}, self.task_id)
        
        return output


    def update_log_file(self, data):
        with open(self.log_file, 'a') as file:
            file.write(data)

    # def connection_report_Table(self, dct_={}, terminal_print=False, ask_when_hosts_fail=False):
    #     table = self.ssh.connection_report_Table(dct=dct_, terminal_print=terminal_print, ask_when_hosts_fail=ask_when_hosts_fail)
    #     return table
    
    def execute(self, host, cmd, only_on_hosts=[], skip_hosts=[], terminal_print='default', tag='',ask_for_confirmation=False, exit_on_fail=True, vendor=None,reconnect_closed_socket=True):
        """
        - Excutes a command on a remove network device
        INPUT:
            1. host -> (string) The host IP
            2. cmd -> (string) The command to run on the remote device
            3. terminal_print -> (string) Print the ouput || error to the terminal, options: ['default', 'json'], default: 'default'
            4. ask_for_confirmation ->  (bool) Ask for confirmation before executing a command, default: False
            5. exit_on_fail ->  (bool) exit the script with code 1 if the command executed with errors  default: True
        OUTPUT: (dictionary)
            - "stdout":    (list) "The output of the command",
            - "stderr":    (list) "The error (Syntax error are detected.)",
            - "exit_code": (int) 0 --> the command run successfully,  1 --> an error occurred
        - does NOT print to the terminal
        """
        class Output:
            def __init__(self):
                self.host = host
                self.cmd = cmd
                self.stdout = None
                self.stderr = None
                self.exit_code = None
        output = Output()

        date_time = datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
        if ask_for_confirmation:
            self.ask_for_confirmation(cmd=self.bcolors.OKBLUE +  cmd + self.bcolors.ENDC)
        
        # Start the execution_time couter
        start_time = time.time()
        # Execute the command
        vendor_ = self.vendor
        if vendor is not None:
            vendor_ = vendor

        run_command = False

        if (len(only_on_hosts) >= 1) and (len(skip_hosts) >= 1):
            rich.print("> You can not use 'onlyOn' and 'skip' together")
            exit(1)
        
        if (len(only_on_hosts) >= 1) and (host in only_on_hosts):
            run_command = True
        
        elif (len(skip_hosts) >= 1) and (host not in skip_hosts):
            run_command = True
        else:
            result = {
                "cmd": [cmd],
                "stdout": [""],
                "stderr": [f"Command execution skipped on {host}, Execute only on: {only_on_hosts} | Skip on: {skip_hosts} "],
                "exit_code": -2
            }

        if (len(only_on_hosts) == 0) and (len(skip_hosts) == 0):
            run_command = True

        print()
        # Print the host IP
        rich.print(Markdown(f"@ **{host}**"))

        # Enter the Privileged mode if needed
        if run_command == True:
            if self.hosts_dct['hosts'][host]['privileged_mode_password']:
                if (not self.hosts_dct['hosts'][host]['privileged_mode']) and (self.hosts_dct['hosts'][host]['is_connected']):
                        rich.print("INFO -- Entering Privileged mode   [ [yellow]...[/yellow] ]", end="\r")
                        # Enter Privileged mode
                        self.exec(host=host, cmd=f"{self.vendor.priviliged_mode_command}\n" + self.hosts_dct['hosts'][host]['privileged_mode_password'], vendor=vendor_,reconnect_closed_socket=reconnect_closed_socket)
                        # Test to enter the "config mode" to test if entering the "Privileged mode" was successful
                        test_config_mode = self.exec(host=host, cmd=f"{self.vendor.configure_mode_command}\n", vendor=vendor_,reconnect_closed_socket=reconnect_closed_socket)
                        # Exit config mode
                        self.exec(host=host, cmd=self.vendor.back_command, vendor=vendor_,reconnect_closed_socket=reconnect_closed_socket)
                        if test_config_mode['exit_code'] == 0:
                            self.hosts_dct['hosts'][host]['privileged_mode'] = True
                            rich.print("INFO -- Entering Privileged mode   [ [green]success[/green] ]")
                        else:
                            rich.print("INFO -- Entering Privileged mode   [ [red]failed[/red] ]")
            result = self.exec(host=host, cmd=cmd, vendor=vendor_,reconnect_closed_socket=reconnect_closed_socket)

        # Calculate the execution_time
        duration = (time.time() - start_time)
        # print()
        
        # Print execution time, exit_code & tag
        rich.print(f'[grey42]Execution time {float("{:.2f}".format(duration))} sec')
        rich.print(f"[grey42]Finished with exit-code of {result['exit_code']}")
        if (tag is not None) and (tag):
            rich.print(f"[grey42]Tag 🏷  '{tag}'")

        # Print the command in blue color
        print(self.bcolors.OKBLUE + '\n'.join(result['cmd']) + self.bcolors.ENDC)

        if terminal_print == 'json':
                formatted_json = json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False)
                colorful_json = highlight(formatted_json.encode('utf8'), lexers.JsonLexer(),  formatters.TerminalFormatter())
                print(colorful_json)

        # Update Log file
        if self.log_output:
            command = '\n\n'.join(result['cmd'])
            out = '\n'.join(result['stdout'])
            error = '\n'.join(result['stderr'])

            data_text = f"""
[ {datetime.today().strftime('%d-%m-%Y %H:%M:%S')} ] [[ excute ]] on {host}
Execution Time: {float("{:.2f}".format(duration))} seconds
The command exited with exit_code of {result['exit_code']}

> command
{command}

> stdout
{out}

> stderr
{error}

--------------------------------------------------------
"""

            data_md = f"""
- [ {datetime.today().strftime('%d-%m-%Y %H:%M:%S')} ] **[[ excute ]] on {host}**
    - Execution Time: {float("{:.2f}".format(duration))} seconds
    - The command exited with exit_code of {result['exit_code']}

> command
```bash
{command}
```

> stdout
```bash
{out}
```
> stderr
```bash
{error}
```

--------------------------------------------------------
"""
            if self.task_log_format == 'txt':
                self.update_log_file(data_text)
            elif self.task_log_format == 'markdown':
                self.update_log_file(data_md)

        if result['exit_code'] == 0:
            if terminal_print == 'default':
                # Print STDOUT in green color
                print(self.bcolors.OKGREEN + '\n'.join(result['stdout']) + self.bcolors.ENDC)     
        else:
            print()
            # Print STDERR in red color
            print(self.bcolors.FAIL + '\n'.join(result['stderr']) + self.bcolors.ENDC)
            print()
            if exit_on_fail:
                print("> Stopped due to the previous error.")
                exit(1)
        output.cmd = result['cmd']
        output.stdout = result['stdout']
        output.stderr = result['stderr']
        output.exit_code = result['exit_code']
        return output
        # return result

    def execute_raw(self, host, cmd, vendor=None):
        """
        - Excutes a command on a remove network device
        INPUT:
            1. host (string) -> The host IP
            2. cmd (string) -> The command to run on the remote device
        OUTPUT: (dictionary)
            - "stdout":    (list) "The output of the command",
            - "stderr":    (list) "The error (Syntax error are detected.)",
            - "exit_code": (int) 0 --> the command run successfully,  1 --> an error occurred
        - does NOT print to the terminal
        """
        vendor_ = self.vendor
        if vendor is not None:
            vendor_ = vendor

        result = self.exec(host, cmd, vendor_)
        class Output:
            def __init__(self):
                self.host = host
                self.cmd = result['cmd']
                self.stdout = result['stdout']
                self.stderr = result['stderr']
                self.exit_code = result['exit_code']
        output = Output()
        return output

    def execute_from_file(self, host, file, terminal_print='default', ask_for_confirmation=False, exit_on_fail=True):
        """
        """
        # Check if the file exists
        if not os.path.exists(file):
            raise SystemExit(f"ERROR -- execute_from_file >> [ {file} ] does NOT exist")

        if not os.path.isfile(file):
            raise SystemExit(f"ERROR -- execute_from_file >> [ {file} ] is NOT a file")

        # Read the file
        try:
            with open(file, 'r') as f:
                file_content = f.read()
                file_content_lines = file_content.split("\n")
                # Remove empty lines
                file_content_lines = [x for x in file_content_lines if x]
        except Exception as e:
            raise SystemExit(f"ERROR -- execute_from_file >> {e}")

        if ask_for_confirmation:
            self.ask_for_confirmation(cmd=self.bcolors.OKBLUE +  file_content + self.bcolors.ENDC)
        
        for cmd in file_content_lines:
            self.execute(host=host, cmd=cmd, terminal_print=terminal_print, ask_for_confirmation=False, exit_on_fail=exit_on_fail)

    def get_config_backup(self, backup_id):
        """
        Method to return config backup
        INPUT:
            - backup_id (string)
        RETURN:
            - file path of the backup (string)
        """
        return self.db.return_backup(backup_id)


    def list_all_tasks(self, all=False, number_to_list=15):
        # The table header
        tasks = []
        # Get list of all the tasks from the DB
        all_tasks_lst =  self.db.tasks_table.all()
        for task in all_tasks_lst:
            # comment = "\n".join(textwrap.wrap(task['format'], width=30, replace_whitespace=False))
            task_name = "\n".join(textwrap.wrap(task['name'], width=26, replace_whitespace=False))
            row = [task['id'], task_name, task['format'], task['n_of_backups'], task['n_of_hosts'], task['n_of_connected_hosts'], task['date'], task['time']]
            tasks.append(row)
        if len(tasks) > number_to_list:
            if not all:
                tasks = tasks[-number_to_list:]
        table = [['id', 'name', 'log format', 'n_of_backups', 'n_of_hosts', 'n_of_connected_hosts', 'date', 'time']]
        tasks.insert(0, table[0])
        out = tabulate(tasks, headers='firstrow', tablefmt='grid', showindex=False)
        return out

    def list_all_backups(self, wide=False, all=False, number_to_list=15):
        backups = []
        all_backups_lst =  self.db.backups_table.all()
        for task in all_backups_lst:
            comment = "\n".join(textwrap.wrap(task['comment'], width=30, replace_whitespace=False))
            if task['success']:
                status = '🟢 success'
            else:
                status = '🔴 failed'
            row = [task['id'], comment, task['host'], task['target'], status, task['date'], task['time']]
            backups.append(row)
        if len(backups) > number_to_list:
            if not all:
                backups = backups[-number_to_list:]
        table = [['id', 'comment', 'host', 'target', 'status','date', 'time']]
        backups.insert(0, table[0])
        out = tabulate(backups, headers='firstrow', tablefmt='grid', showindex=False)
        return out

    def delete_task(self, task_id):
        """
        Delete a task
        INPUT:
            - task id (string)
        """
        try:
            Task = Query()
            task_dct = self.db.tasks_table.search(Task.id == task_id)[0]
        except IndexError as e:
            print("ERROR -- Could NOT find the task >> Possible invalid task ID")
            exit(1)
       
        try:
            # Remove the file
            os.remove(task_dct['log_file'])
        except (OSError, TypeError) as e:
            # If the file is NOT found, just ignore it and delete the record from the DB.
            print(f"INFO -- task file not found '{task_dct['log_file']}', deleting the record from the DB")
        
        # Delete the backup from the DB
        self.db.delete_tasks_table(task_id)
        print(f"INFO -- task with name '{task_dct['name']}' deleted successfully")
        exit(0)

        

        print(Task)
        exit(0)

    def delete_config_backup(self, backup_id):
        """
        Delete a config backup
        INPUT:
            - backup id (string)
        """
        # Get backup file path
        try:
            Backup = Query()
            backup_dct = self.db.backups_table.search(Backup.id == backup_id)[0]
        except IndexError as e:
            print("ERROR -- Could NOT find the backup >> Possible invalid backup ID")
            exit(1)

        if backup_dct['target'] == 'local':
            try:
                # Remove the file
                os.remove(backup_dct['location'])
            except OSError as e:
                # If the file is NOT found, just ignore it and delete the record from the DB.
                print(f"INFO -- could not delete file '{backup_dct['location']}', deleting the record from the DB")
            
            # Delete the backup from the DB
            self.db.delete_backups_table(backup_id)
            print(f"INFO -- backup with comment '{backup_dct['comment']}' deleted successfully, Host: {backup_dct['host']} , Target: {backup_dct['target']}")
            exit(0)

        if backup_dct['target'] == 's3':
            print("Deleting S3 backups is not supported yet.")
            exit(0)


    def take_config_backup(self, host, comment, privileged_mode_password="", exit_on_fail=False, target='local'):
        """
        Take full configurations backup of the device
        """
        class Output:
            def __init__(self):
                self.exit_code = 1
                self.stderr = ""
                self.stdout = ""
                self.location = ""
                self.id = ""
        output = Output()

        start_time = time.time()

        print("\n@ {}".format(host))
        if self.hosts_dct['hosts'][host]['privileged_mode_password']:
                if (not self.hosts_dct['hosts'][host]['privileged_mode']) and (self.hosts_dct['hosts'][host]['is_connected']):
                        rich.print("INFO -- Entering Privileged mode   [ [yellow]...[/yellow] ]", end="\r")
                        # Enter Privileged mode
                        self.exec(host=host, cmd=f"{self.vendor.priviliged_mode_command}\n" + self.hosts_dct['hosts'][host]['privileged_mode_password'], vendor=self.vendor,reconnect_closed_socket=True)
                        # Test to enter the "config mode" to test if entering the "Privileged mode" was successful
                        test_config_mode = self.exec(host=host, cmd=f"{self.vendor.configure_mode_command}\n", vendor=self.vendor,reconnect_closed_socket=True)
                        # Exit config mode
                        self.exec(host=host, cmd="exit", vendor=self.vendor,reconnect_closed_socket=True)
                        if test_config_mode['exit_code'] == 0:
                            self.hosts_dct['hosts'][host]['privileged_mode'] = True
                            rich.print("INFO -- Entering Privileged mode   [ [green]success[/green] ]")
                        else:
                            rich.print("INFO -- Entering Privileged mode   [ [red]failed[/red] ]")

        if not self.hosts_dct['hosts'][host]['privileged_mode_password']:
            print("WARNING -- No 'privileged_mode_password' provided, skipping taking the backup")
            output.exit_code = 1
            output.stderr = "No 'privileged_mode_password' provided, skipping taking the backup"
            output.stdout = "failed"
            if exit_on_fail:
                    exit(1)
            return output
        else:
            # - test to run the command
            #   - If failed, try to enter the priviliged mode and run the command again

            # Run the backup command
            # print("INFO -- Running the backup command")
            backup_cmd_result = self.execute_raw(host=host, cmd=self.vendor.backup_command,)
            
            output.exit_code = 0
            if backup_cmd_result.exit_code == 1:
                output.exit_code = 1
                
                #
                #  Enter the priviled mode eg. ('enable' command in Cisco)
                # print("INFO -- Entering priviliged mode")

                # enter_privileged_mode_cmd_result = self.execute_raw(host=host, cmd= f'{self.vendor.priviliged_mode_command}\n' + privileged_mode_password)
                # if enter_privileged_mode_cmd_result.exit_code == 1:
                #     print(f"ERROR -- Failed to enter the priviled mode while getting config backup with comment: {comment}")
                #     print(self.bcolors.FAIL + "\n".join(enter_privileged_mode_cmd_result.stderr) + self.bcolors.ENDC)
                #     output.stderr = f"Failed to enter the priviled mode while getting config backup with comment: {comment}"
                #     output.stdout = "failed"
                #     if exit_on_fail:
                #         exit(1)
                #     return output
                # else:
                #     # Run the backup command again
                #     print("INFO -- Running the backup command again")
                #     backup_cmd_result = self.execute_raw(host=host, cmd=self.vendor.backup_command,)
                #     self.execute_raw(host, "end")
                #     output.exit_code = 0

        # Inserting the DB record
        # Generate a backup ID
        self.backup_id = str(uuid.uuid4())
        output.id = self.backup_id
        date = datetime.today().strftime('%d-%m-%Y')
        time_ = datetime.today().strftime('%H:%M:%S')
        self.db.insert_backups_table({'id': self.backup_id, 
                                   'comment': comment,
                                   'task': self.task_id,
                                   'host': host,
                                   'target': target,
                                   'location': '',
                                   'date': date, 
                                   'time': time_,
                                   'success': False,
                                   'failed_reason': ''
                                   })

        # Start storing the backup
        # If the backup commaned executed successfully
        if backup_cmd_result.exit_code == 0:
            # Clean the backup output [ Remove the backup commands ]
            backup_output = '\n'.join(backup_cmd_result.stdout)
            for c in self.vendor.backup_command.split("\n"):
                backup_output = backup_output.replace(c.lstrip().strip(), '')
                backup_output = backup_output.strip()

            backup_file = str(host) + '-{}.txt'.format(uuid.uuid4().hex.upper()[0:10])
            output.location = self.log_and_backup_dir + "/" + backup_file
            
            # Update Log file
            date_time = datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
            duration = (time.time() - start_time)
            if self.log_output:
                out = '\n'.join(backup_cmd_result.stdout)
                error = '\n'.join(backup_cmd_result.stderr)
                data_text = f"""
[ {datetime.today().strftime('%d-%m-%Y %H:%M:%S')} ] [[ backup_config ]] on {host}
Execution Time: {float("{:.2f}".format(duration))} seconds
The backup taken successfully
Backup Comment: {comment}
Backup ID: {self.backup_id}

--------------------------------------------------------
"""

                data_md = f"""
- [ {datetime.today().strftime('%d-%m-%Y %H:%M:%S')} ] [[ backup_config ]] on {host}
    - Execution Time: {float("{:.2f}".format(duration))} seconds
    - The backup taken successfully
    - Backup Comment: {comment}
    - Backup ID: {self.backup_id}

--------------------------------------------------------
"""
                if self.task_log_format == 'txt':
                    self.update_log_file(data_text)
                elif self.task_log_format == 'markdown':
                    self.update_log_file(data_md)

            def save_backup_locally(b_dir=self.log_and_backup_dir, b_file=backup_file):
                try:
                    b_file = b_dir +  '/' + b_file
                    # The 'local' target stores the backup to file on the local machine
                    # Create the backup dir
                    if not os.path.isdir(b_dir):
                        Path(b_dir).mkdir(parents=True, exist_ok=True)
                    # Create the backup file
                    with open(b_file, 'w') as file:
                        # Writing the backup to a file
                        file.write(backup_output)
                except FileNotFoundError as e:
                    rich.print("ERROR -- Failed to backup config with comment [ {} ]".format(comment))
                    print("ERROR -- Failed to write backup to file \n> {}".format(e))
                    if exit_on_fail:
                        exit(1)
            if target == 'local':
                save_backup_locally(b_dir=self.log_and_backup_dir)
                # Updating the loaction key with the backup location
                self.db.update_backups_table({'location': self.log_and_backup_dir + "/" + backup_file}, self.backup_id)
            if target == 's3':
                s3 = S3_APIs()
                # Create a temp_file and save the backup to it
                save_backup_locally(b_dir='/tmp')
                # Upload the backup to s3
                #backup stored here
                # print('/tmp/' + backup_file)

                # Check if the bucket exists (the bucket specified int the config file)
                if not s3.bucket_exists(s3.bucket):
                    # print(s3.s3_client.get_bucket_acl(Bucket=s3.bucket))
                    # If specified in the configuration file to create the bucket if it does NOT exist.
                    if s3.create_bucket_if_does_not_exist:
                        # Create the bucket
                        if s3.region == 'default':
                            create_bucket = s3.create_bucket(bucket_name=s3.bucket)
                        else:
                            create_bucket = s3.create_bucket(bucket_name=s3.bucket, region=s3.region)
                        if not create_bucket['success']:
                            raise SystemExit(f"ERROR -- Failed to create bucket: [ {s3.bucket} ]\n> {create_bucket['fail_reason']}")
                        else:
                            print(f"INFO -- Bucket [ {s3.bucket} ] created successfully")
                    else:
                        raise SystemExit(f"ERROR -- bucket [ {s3.bucket} ] does NOT exist.")

                # upload the backup
                upload_backup_file = s3.upload_file(bucket=s3.bucket, file_path='/tmp/' + backup_file, directory=datetime.today().strftime('%d-%m-%Y'))
                if upload_backup_file['success']:
                    # Remove the temp backup file
                    os.remove('/tmp/' + backup_file)
                    # Update the DB
                    # For S3 targets -> location row is a list; the 0 index contains the bucket & the 1 index contains the key
                    self.db.update_backups_table({'location': [s3.bucket, datetime.today().strftime('%d-%m-%Y') + '/' + backup_file]}, self.backup_id)
  
                else:
                    print("ERROR -- Failed to backup config with comment [ {} ]".format(comment))
                    # Update the DB with the fail_reason
                    self.db.update_backups_table({'fail_reason': upload_backup_file['fail_reason']}, self.backup_id)
                    # Remove the temp backup file
                    os.remove('/tmp/' + backup_file)
                    raise SystemExit(f"> Failed to upload the backup to S3 >> {upload_backup_file['fail_reason']}")


        # Update the backup to the task table .. Add the backup ID to the 
        self.db.append_backups_ids_tasks_table('backups_ids', self.backup_id, self.task_id)
        # Increament the backups number in the task by 1
        self.db.increment_key_tasks_table('n_of_backups', self.task_id)

        ## Terminal printing ##
        if backup_cmd_result.exit_code == 0:
            print("INFO -- backup taken successfully  [ {} ]".format(comment))
            self.db.update_backups_table({'success': True}, self.backup_id)
        else:
            self.db.update_backups_table({'success': False}, self.backup_id)
            self.db.update_backups_table({'failed_reason': backup_cmd_result.stderr}, self.backup_id)

            print("ERROR -- Failed to backup config with comment [ {} ]".format(comment))
            print(self.bcolors.FAIL + '\n'.join(backup_cmd_result.stderr) + self.bcolors.ENDC)
            output.exit_code = 1
            output.stderr = '\n'.join(backup_cmd_result.stderr)
            output.stdout = "failed"
            if exit_on_fail:
                exit(1)
            # raise SystemExit(self.bcolors.FAIL + '\n'.join(backup_cmd_result.stderr) + self.bcolors.ENDC)
        # output.stdout = "success"
        return output

    # def execute_test(self, hosts_list, cmd, parallel=False, parallel_threads=5):
    #     """
    #     Testing
    #     """
    #     if not parallel:
    #         for host in hosts_list.keys():
    #             if self.hosts_dct['hosts'][host]['is_connected']:
    #                 # Test close the connection
    #                 self.close_channel(host)
    #                 self.execute(host=host, cmd=cmd)
    #             else:
    #                 if self.debug:
    #                     rich.print(f"\nDEBUG -- [bold]HOST:[/bold] {host} skip_hostsped, [bold]REASON[/bold]: [bright_red]{self.hosts_dct['hosts'][host]['fail_reason']}[/bright_red]")
    #                     rich.print(self.hosts_dct['hosts'][host])


    # def execute_on_group(self, group, cmd, parallel=False, parallel_threads=5):
    #     """
    #     Testing
    #     """
    #     # Authenticate
    #     self.authenticate(groups=[group], user='orange', password='cisco', port=1114, terminal_print=True)

    #     if not isinstance(cmd, list):
    #         cmd = [cmd]
    
    #     if not parallel:
    #         # Execute with a loop
    #         for host in self.hosts_dct['hosts'].keys():
    #             # Execute on only the authenticated devices
    #             if self.hosts_dct['hosts'][host]['is_connected']:
    #                 # Test close the connection
    #                 # self.close_channel(host)
    #                 for command in cmd:
    #                     self.execute(host=host, cmd=command)
    #             else:
    #                 if self.debug:
    #                     rich.print(f"\nDEBUG -- [bold]HOST:[/bold] {host} skip_hostsped, [bold]REASON[/bold]: [bright_red]{self.hosts_dct['hosts'][host]['fail_reason']}[/bright_red]")
    #                     rich.print(self.hosts_dct['hosts'][host])

    def read_env_key(self, key):
        """
        Read Environment Variable
        INPUT:
            - Key (string)
        Return:
            - Key's Value
        """
        try:
            value = os.environ[key]
            return value
        except KeyError as e:
            raise SystemExit(f"ERROR -- Env Key '{key}' does NOT exist")
    
    def sub_task(self, group, username, password, privileged_mode_password, port=22,reconnect=False, cmds=[], name="", vendor='cisco', parallel=False, take_config_backup_dct={}):
        """
        Testing
        INPUT:
            1. group (string) group name to authenticate
            2. cmds (list of dcts) commands to execute        
        """
        # dct to store the executed commands results (of the sub task)
        commands_executed_dct = {}

        # Authenticate
        self.authenticate(groups=[group], user=username, password=password, privileged_mode_password=privileged_mode_password, port=port, terminal_print=True)

        if not isinstance(cmds, list):
            cmds = [cmds]

        # Abort of there is no commands to execute
        if len(cmds) < 1:
            rich.print("INFO -- No commands to execute")
            exit(0)
        
        if name:
            rich.print(Markdown(f"### Sub-Task: {name}", style="bold"))
            rich.print(Rule(style='#AAAAAA'))
        
        # Use a loop to execute the commands on the hosts
        if not parallel:
            # Execute with a loop
            for host in self.hosts_dct['hosts'].keys():

                # Take config backup
                rich.print(take_config_backup_dct)
                if take_config_backup_dct.get('comment'):
                    self.take_config_backup(host=host, comment=take_config_backup_dct.get('comment'), privileged_mode_password=privileged_mode_password, exit_on_fail=False, target=take_config_backup_dct.get('target'))

                # Execute on only the authenticated devices
                if self.hosts_dct['hosts'][host]['is_connected']:
                    # Test close the connection
                    # self.close_channel(host)
                    for command_dct in cmds:
                        run_command = False
                        # Flag for the command tag name
                        tag = None
                        # Getting the tag name if was provided
                        if 'tag' in command_dct:
                            tag = command_dct['tag']
                        
                        # Before execution
                        # Evaluate the "when" condition
                        if ('when' in command_dct) and (command_dct['when']['tag']):
                            when_condition_dct = command_dct.get('when')
                            
                            # Check the provided operator
                            if 'operator' in when_condition_dct:
                                if when_condition_dct['operator'] not in ['is', 'is_not']:
                                    rich.print(f"\nERROR -- command condition operator only supports {['is', 'is_not']} You've provided ({when_condition_dct['operator']})")
                                    exit(1)
                            else:
                                # set the default operator as 'is'
                                when_condition_dct['operator'] = 'is'
                            try:
                                # check if the "tag" exists
                                if when_condition_dct['tag'] in commands_executed_dct:
                                    # Get the results of the commaned with the tag
                                    condition_command = commands_executed_dct.get(when_condition_dct['tag'])
                                    
                                    grid = Table.grid(expand=True)
                                    grid.add_column(ratio=2)
                                    grid.add_row(f"[grey42]Condition command exited with {commands_executed_dct.get(when_condition_dct['tag'])['exit_code']} ")

                                    if when_condition_dct.get('operator') == 'is_not':
                                        if condition_command['exit_code'] != when_condition_dct['exit_code']:
                                            run_command = True
                                    else:
                                        if condition_command['exit_code'] == when_condition_dct['exit_code']:
                                            run_command = True
                                else:
                                    print()
                                    # Print the command
                                    print(self.bcolors.OKBLUE +  command_dct['command'] + self.bcolors.ENDC)
                                    raise SystemExit(f"ERROR -- at 'when' condition {when_condition_dct} -> provided tag not found")
                            except KeyError as e:
                                rich.print(f"ERROR -- Key not found  > {e}")

                            if run_command:
                                exec_cmd = self.execute(host=host, tag=tag,cmd=command_dct['command'], reconnect_closed_socket=reconnect, exit_on_fail=command_dct['exit_on_fail'], ask_for_confirmation=command_dct['ask_for_confirmation'], only_on_hosts=command_dct['onlyOn'], skip_hosts=command_dct['skip'])
                                # Recording commands that has ID specified
                                try:
                                    if tag:
                                        commands_executed_dct[tag] = {
                                            "command": command_dct['command'],
                                            "exit_code": exec_cmd.exit_code,
                                            "stderr": exec_cmd.stderr,
                                            "stdout": exec_cmd.stdout
                                        }
                                except:
                                    pass
                            else:
                                print()
                                # Print the command
                                rich.print(Markdown(f"@ **{host}**"))
                                print(self.bcolors.OKBLUE +  command_dct['command'] + self.bcolors.ENDC)
                                rich.print(Markdown("> command execution skipped due to condition:") ,
                                           Markdown(f" - Execute only when 'exit_code' of command with tag 🏷 '{when_condition_dct['tag']}' {when_condition_dct['operator']} '{when_condition_dct['exit_code']}'"))
                                print()
                                # rich.print(f"[bold]✋ command execution skipped due to condition:[/bold]  \n   => Execute only when 'exit_code' of command with tag 🏷 '{when_condition_dct['tag']}' {when_condition_dct['operator']} '{when_condition_dct['exit_code']}'")
                                # rich.print(Panel.fit(grid,border_style="grey42"))

                        else:
                            exec_cmd = self.execute(host=host, tag=tag,cmd=command_dct['command'], reconnect_closed_socket=reconnect, exit_on_fail=command_dct['exit_on_fail'], ask_for_confirmation=command_dct['ask_for_confirmation'], only_on_hosts=command_dct['onlyOn'], skip_hosts=command_dct['skip'])
                            # Recording commands that has ID specified
                            if tag:
                                commands_executed_dct[tag] = {
                                    "command": command_dct['command'],
                                    "exit_code": exec_cmd.exit_code,
                                    "stderr": exec_cmd.stderr,
                                    "stdout": exec_cmd.stdout
                                }
                else:
                    if self.debug:
                        rich.print(f"\nDEBUG -- [bold]HOST:[/bold] {host} skip_hostsped, [bold]REASON[/bold]: [bright_red]{self.hosts_dct['hosts'][host]['fail_reason']}[/bright_red]")
                        rich.print(self.hosts_dct['hosts'][host])
                        
                        