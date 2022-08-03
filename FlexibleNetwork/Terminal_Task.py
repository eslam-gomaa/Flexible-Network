from pytest import skip
from FlexibleNetwork.Vendors import Cisco
from FlexibleNetwork.Flexible_Network import ReadCliOptions
from FlexibleNetwork.Flexible_Network import CLI
from FlexibleNetwork.Flexible_Network import Config
from FlexibleNetwork.Flexible_Network import Inventory
from FlexibleNetwork.Flexible_Network import SSH_connection
from FlexibleNetwork.Flexible_Network import SSH_Authentication
from FlexibleNetwork.Integrations import RocketChat_API
from FlexibleNetwork.Integrations import S3_APIs
from FlexibleNetwork.Integrations import Cyberark_APIs_v2
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
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.console import Console, Group
from rich.rule import Rule

class Terminal_Task(SSH_Authentication):

    task_name = None # Should be updated from a cli option. --name

    def __init__(self):
        super().__init__(debug=ReadCliOptions.debug)

        # Initialize the "CLI" class so that it read the cli options 
        cli = CLI()
        cli.argparse()
        
        # Initialize the DB because we'll need it if '--task list' or '--backup list' are specified
        self.db = TinyDB_db()

        # If --task is specified
        if ReadCliOptions.list_tasks:
            print(self.db.list_all_tasks())
            exit(0)

        self.debug = ReadCliOptions.debug

        # If --backup is specified
        if ReadCliOptions.list_backups:
            print(self.db.list_all_backups())
            exit(0)

        if ReadCliOptions.get_log is not None:
            print(self.db.get_task_log(ReadCliOptions.get_log))

        if ReadCliOptions.get_backup is not None:
            print(self.db.return_backup(ReadCliOptions.get_backup))


        # Initialize the "Config" class so that it checks the config file at the begining. 
        config = Config()
        self.validate_integrations()
        self.inventory = Inventory()
        self.vendor = Cisco() # Default vendor class should exist in the config
        self.ssh = SSH_connection()
        self.ssh.vendor = self.vendor
        self.bcolors = Bcolors()

        
        self.local_db_dir = self.db.local_db_dir
        self.log_and_backup_dir = self.local_db_dir +  '/' + datetime.today().strftime('%d-%m-%Y')
        # Gernate the task id
        self.task_id = str(uuid.uuid4())
        self.log_file = self.log_and_backup_dir + '/' + self.task_id + '.txt'
        # Get the task name
        self.task_name = str(ReadCliOptions.task_name)
        # By default do NOT log the output,
        # this will be set to True if number_of_authenticated_devices > 0
        self.log_output = False
        self.log_output_file = None
        # create a row in the tasks table & add the id & name
        date = datetime.today().strftime('%d-%m-%Y')
        time = datetime.today().strftime('%H-%M-%S')
        self.db.insert_tasks_table({'id': self.task_id, 
                                   'name': self.task_name,
                                   'comment': 'to be done >> as a cli option.',
                                   'n_of_backups': 0, 
                                   'backups_ids': [],
                                   'log_file': None,
                                   'date': date, 
                                   'time': time,
                                   'full_devices_n': 0,
                                   'authenticated_devices_n': 0
                                   })


        # Read all inventory sections
        # self.inventory = self.inventory.read_inventory()
        self.inventory_groups = self.inventory.read_inventory()
        self.inventory_groups_names = []
        for i in self.inventory_groups.keys():
            self.inventory_groups_names.append(i)

        self.devices_dct = {}
        self.connected_devices_dct = {}
        self.total_connected_devices_dct = {}
        self.connected_devices_number = 0
        self.connection_failed_devices_number = 0
        self.group_to_authenticate_from_cli = ReadCliOptions.authenticate_group
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

    def authenticate(self, groups, user, password, port=22, terminal_print=True):
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

        # groups.append('pa4')

        for group in groups:
            # Authenticate group
            group_hosts = self.inventory.get_section(group)
            auth = self.authenticate_hosts(hosts=group_hosts, group_name=group, user=user, password=password, port=port, terminal_print=terminal_print, debug=self.debug)
            # dct that contains each device info (where the key is the device IP)
            # rich.print(self.hosts_dct)
            # rich.print(SSH_Authentication.hosts_dct)
            # exit(1)
            self.devices_dct = {}
            self.devices_dct = auth.get('hosts')
            
            self.connected_devices_dct = self.ssh.connected_devices_dct
            self.total_connected_devices_dct = dict(self.total_connected_devices_dct, **self.connected_devices_dct)
            self.full_devices_number = len(group_hosts)
            self.connected_devices_number = self.ssh.connected_devices_number
            self.connection_failed_devices_number = self.ssh.connection_failed_devices_number
            self.db.update_tasks_table({'full_devices_n': self.full_devices_number}, self.task_id)
            self.db.update_tasks_table({'authenticated_devices_n': self.connected_devices_number}, self.task_id)
            if terminal_print:
                if ReadCliOptions.no_confirm_auth:
                    ask_when_hosts_fail_ = False
                else:
                    ask_when_hosts_fail_ = True
                self.connection_report_Table(dct=self.devices_dct, terminal_print=True, ask_when_hosts_fail=ask_when_hosts_fail_)
            # If connected_devices_number > 0 , set the log_output flag to True
            if self.connected_devices_number > 0:
                self.log_output = True
                if not os.path.isdir(self.log_and_backup_dir):
                    Path(self.log_and_backup_dir).mkdir(parents=True, exist_ok=True)
                self.db.update_tasks_table({'log_file': self.log_file}, self.task_id)
            else:
                self.db.update_tasks_table({'log_file': None}, self.task_id)

        

    def update_log_file(self, data):
        with open(self.log_file, 'a') as file:
            file.write(data)

    # def connection_report_Table(self, dct_={}, terminal_print=False, ask_when_hosts_fail=False):
    #     table = self.ssh.connection_report_Table(dct=dct_, terminal_print=terminal_print, ask_when_hosts_fail=ask_when_hosts_fail)
    #     return table
    
    def execute(self, host, cmd, only_on_hosts, skip_hosts, terminal_print='default', tag='',ask_for_confirmation=False, exit_on_fail=True, vendor=None,reconnect_closed_socket=True):
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
        
        date_time = datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
        if ask_for_confirmation:
            self.ask_for_confirmation(cmd=self.bcolors.OKBLUE +  cmd + self.bcolors.ENDC)
        
        # Start the execution_time couter
        start_time = time.time()
        # Execute the command
        vendor_ = self.vendor
        if vendor is not None:
            vendor_ = vendor

        if (len(only_on_hosts) >= 1) and (len(skip_hosts) >= 1):
            rich.print("> You can not use 'onlyOn' and 'skip' together")
            exit(1)
        
        if (len(only_on_hosts) >= 1) and (host in only_on_hosts):
            result = self.exec(host=host, cmd=cmd, vendor=vendor_,reconnect_closed_socket=reconnect_closed_socket)
        
        elif (len(skip_hosts) >= 1) and (host not in skip_hosts):
            result = self.exec(host=host, cmd=cmd, vendor=vendor_,reconnect_closed_socket=reconnect_closed_socket)
        else:
            result = {
                "cmd": [cmd],
                "stdout": [""],
                "stderr": [f"Command execution skipped on {host}, Execute only on: {only_on_hosts} | Skip on: {skip_hosts} "],
                "exit_code": -2
            }

        if (len(only_on_hosts) == 0) and (len(skip_hosts) == 0):
            result = self.exec(host=host, cmd=cmd, vendor=vendor_,reconnect_closed_socket=reconnect_closed_socket)


        # Calculate the execution_time
        duration = (time.time() - start_time)
        # print()
        
        print()
        rich.print(Markdown(f"@ **{host}**"))
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
            command = '\n'.join(result['cmd'])
            output = '\n'.join(result['stdout'])
            error = '\n'.join(result['stderr'])
            data = f"""\n@ {host}
[[ excute ]]
Time: {date_time}
Execution Time: {float("{:.2f}".format(duration))} seconds
The command exited with exit_code of {result['exit_code']}
>> {command}

{output}
{error}

--------------------------------------------------------
"""
            self.update_log_file(data)

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
        return result

    def execute_raw(self, host, cmd):
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
        result = self.ssh.exec(host, cmd, self.vendor)
        return result

    def execute_from_file(self, host_dct, file, terminal_print='default', ask_for_confirmation=False, exit_on_fail=True):
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
            self.ssh.ask_for_confirmation(cmd=self.bcolors.OKBLUE +  file_content + self.bcolors.ENDC)
        
        for cmd in file_content_lines:
            self.execute(host_dct=host_dct, cmd=cmd, terminal_print=terminal_print, ask_for_confirmation=False, exit_on_fail=exit_on_fail)


    def backup_config(self, host_dct, comment, target='local'):
        """
        Take full configurations backup of the device
        """
        start_time = time.time()
        result = self.ssh.backup_config(host_dct)

        # Inserting the DB record
        # Generate a backup ID
        self.backup_id = str(uuid.uuid4())
        date = datetime.today().strftime('%d-%m-%Y')
        time_ = datetime.today().strftime('%H-%M-%S')
        self.db.insert_backups_table({'id': self.backup_id, 
                                   'comment': comment,
                                   'task': self.task_id,
                                   'host': host_dct['host'],
                                   'target': target,
                                   'location': '',
                                   'date': date, 
                                   'time': time_,
                                   'success': False,
                                   'failed_reason': ''
                                   })

        # Start storing the backup
        # If the backup commaned executed successfully
        if result['exit_code'] == 0:
            # Clean the backup output [ Remove the backup commands ]
            backup_output = '\n'.join(result['stdout'])
            for c in self.vendor.backup_command.split("\n"):
                backup_output = backup_output.replace(c.lstrip().strip(), '')
                backup_output = backup_output.strip()

            backup_file = host_dct['host'] + '-{}.txt'.format(uuid.uuid4().hex.upper()[0:10])

            
            # Update Log file
            date_time = datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
            duration = (time.time() - start_time)
            if self.log_output:
                output = '\n'.join(result['stdout'])
                error = '\n'.join(result['stderr'])
                data = f"""\n@ {host_dct['host']}
[[ backup_config ]]
@ {host_dct['host']}
Time: {date_time}
Execution Time: {float("{:.2f}".format(duration))} seconds
The backup taken successfully
Backup Comment: {comment}
Backup ID: {self.backup_id}

--------------------------------------------------------
"""
                self.update_log_file(data)


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
                    print("ERROR -- Failed to backup config > [ {} ]".format(comment))
                    print("ERROR -- Failed to write backup to file \n> {}".format(e))
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
                    print("ERROR -- Failed to backup config > [ {} ]".format(comment))
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
        print("\n@ {}".format(host_dct['host']))
        if result['exit_code'] == 0:
            print("> backup taken successfully > [ {} ]".format(comment))
            self.db.update_backups_table({'success': True}, self.backup_id)
        else:
            self.db.update_backups_table({'success': False}, self.backup_id)
            self.db.update_backups_table({'failed_reason': result['stderr']}, self.backup_id)

            print("ERROR -- Failed to backup config > [ {} ]".format(comment))
            raise SystemExit(self.bcolors.FAIL + '\n'.join(result['stderr']) + self.bcolors.ENDC)


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


    def execute_on_group(self, group, cmd, parallel=False, parallel_threads=5):
        """
        Testing
        """
        # Authenticate
        self.authenticate(groups=[group], user='orange', password='cisco', port=1114, terminal_print=True)

        if not isinstance(cmd, list):
            cmd = [cmd]
    
        if not parallel:
            # Execute with a loop
            for host in self.hosts_dct['hosts'].keys():
                # Execute on only the authenticated devices
                if self.hosts_dct['hosts'][host]['is_connected']:
                    # Test close the connection
                    # self.close_channel(host)
                    for command in cmd:
                        self.execute(host=host, cmd=command)
                else:
                    if self.debug:
                        rich.print(f"\nDEBUG -- [bold]HOST:[/bold] {host} skip_hostsped, [bold]REASON[/bold]: [bright_red]{self.hosts_dct['hosts'][host]['fail_reason']}[/bright_red]")
                        rich.print(self.hosts_dct['hosts'][host])

    
    def sub_task(self, group, username, password, port=22,reconnect=False, cmds=[], name="", vendor='cisco', parallel=False):
        """
        Testing
        INPUT:
            1. group (string) group name to authenticate
            2. cmds (list of dcts) commands to execute        
        """
        # dct to store the executed commands results (of the sub task)
        commands_executed_dct = {}

        # Authenticate
        self.authenticate(groups=[group], user='orange', password='cisco', port=1113, terminal_print=True)

        if not isinstance(cmds, list):
            cmds = [cmds]
        
        # Abort of there is no commands to execute
        if len(cmds) < 1:
            rich.print("INFO -- No commands to execute")
            exit(0)
        
        if name:
            rich.print(Markdown(f"### Sub-Task: {name}", style="bold"))
            rich.print(Rule(style='#AAAAAA'))
        
        if not parallel:
            # Execute with a loop
            for host in self.hosts_dct['hosts'].keys():
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
                        # Evaluate the when condition
                        if ('when' in command_dct) and (command_dct['when']['tag']):
                            when_condition_dct = command_dct.get('when')

                            # check if the tag exists
                            if 'operator' in when_condition_dct:
                                if when_condition_dct['operator'] not in ['is', 'is_not']:
                                    rich.print(f"\nERROR -- command condition operator only supports {['is', 'is_not']} You've provided ({when_condition_dct['operator']})")
                                    exit(1)
                            else:
                                # set the default operator as 'is'
                                when_condition_dct['operator'] = 'is'
                            try:
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
                                    tag_ = command_dct['tag']
                                    if tag:
                                        commands_executed_dct[tag_] = {
                                            "command": command_dct['command'],
                                            "exit_code": exec_cmd['exit_code'],
                                            "stderr": exec_cmd['stderr'],
                                            "stdout": exec_cmd['stdout']
                                        }
                                except:
                                    pass
                            else:
                                print()
                                # Print the command
                                rich.print(Markdown(f"@ **{host}**"))
                                print(self.bcolors.OKBLUE +  command_dct['command'] + self.bcolors.ENDC)
                                rich.print(f"[bold]🔲 command skip_hostsped due to condition:[/bold]  [ [yellow]execute only when 'exit_code' of command with tag 🏷 '{when_condition_dct['tag']}' {when_condition_dct['operator']} '{when_condition_dct['exit_code']}'[/yellow] ]")
                                # rich.print(Panel.fit(grid,border_style="grey42"))


                        else:
                            exec_cmd = self.execute(host=host, tag=tag,cmd=command_dct['command'], reconnect_closed_socket=reconnect, exit_on_fail=command_dct['exit_on_fail'], ask_for_confirmation=command_dct['ask_for_confirmation'], only_on_hosts=command_dct['onlyOn'], skip_hosts=command_dct['skip'])
                            # Recording commands that has ID specified
                            try:
                                tag_ = command_dct['tag']
                                if tag:
                                    commands_executed_dct[tag_] = {
                                        "command": command_dct['command'],
                                        "exit_code": exec_cmd['exit_code'],
                                        "stderr": exec_cmd['stderr'],
                                        "stdout": exec_cmd['stdout']
                                    }
                            except:
                                pass
                else:
                    if self.debug:
                        rich.print(f"\nDEBUG -- [bold]HOST:[/bold] {host} skip_hostsped, [bold]REASON[/bold]: [bright_red]{self.hosts_dct['hosts'][host]['fail_reason']}[/bright_red]")
                        rich.print(self.hosts_dct['hosts'][host])
                        
                        