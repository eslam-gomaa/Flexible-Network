from FlexibleNetwork.Vendors import Cisco
from FlexibleNetwork.Flexible_Network import ReadCliOptions
from FlexibleNetwork.Flexible_Network import CLI
from FlexibleNetwork.Flexible_Network import Config
from FlexibleNetwork.Flexible_Network import Inventory
from FlexibleNetwork.Flexible_Network import SSH_connection
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

class Terminal_Task:
    task_name = None # Should be updated from a cli option. --name

    def __init__(self):
        # Initialize the "CLI" class so that it read the cli options 
        cli = CLI()
        cli.argparse()
        
        # Initialize the DB because we'll need it if '--task list' or '--backup list' are specified
        self.db = TinyDB_db()

        # If --task is specified
        if ReadCliOptions.list_tasks:
            print(self.db.list_all_tasks())
            exit(0)

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
        inventory = Inventory()
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
        # self.inventory = inventory.read_inventory()
        self.inventory_groups = inventory.read_inventory()
        self.devices_dct = {}
        self.connected_devices_dct = {}
        self.connected_devices_number = 0
        self.connection_failed_devices_number = 0
        if ReadCliOptions.authenticate_group:
            # Get the IPs of the section to the 'self.inventory' attribute
            self.inventory = inventory.get_section(ReadCliOptions.authenticate_group)
            # If the section not found the 'get_section' method will return None
            # Hence the script will exit with code 1
            if self.inventory is None:
                print("\nERROR -- Inventory section [ {} ] does NOT exist !".format(ReadCliOptions.authenticate_group))
                exit(1)
            # Stop if the choosen group is empty
            if not self.inventory:
                print("\n> The choosen group [ {} ] has no hosts .. No need to continue.".format(ReadCliOptions.authenticate_group))
                exit(0)
            # Read the user, password, port 
            self.user = ReadCliOptions.auth_user
            self.password = ReadCliOptions.auth_password
            # Default port is 22 if not specified in the CLI
            self.port = ReadCliOptions.auth_port
            # Authenticate the choosen group
            self.authenticate(hosts=self.inventory, user=self.user, password=self.password, port=self.port)
            
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

    def authenticate(self, hosts, user, password, port, terminal_print=True):
        self.ssh.authenticate(hosts=hosts, user=user, password=password, port=port, terminal_print=terminal_print)
        self.devices_dct = self.ssh.devices_dct
        self.connected_devices_dct = self.ssh.connected_devices_dct
        self.full_devices_number = len(hosts)
        self.connected_devices_number = self.ssh.connected_devices_number
        self.connection_failed_devices_number = self.ssh.connection_failed_devices_number
        self.db.update_tasks_table({'full_devices_n': self.full_devices_number}, self.task_id)
        self.db.update_tasks_table({'authenticated_devices_n': self.connected_devices_number}, self.task_id)
        if terminal_print:
            if ReadCliOptions.no_confirm_auth:
                ask_when_hosts_fail_ = False
            else:
                ask_when_hosts_fail_ = True
            self.ssh.connection_report_Table(dct=self.devices_dct, terminal_print=True, ask_when_hosts_fail=ask_when_hosts_fail_)
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

    def connection_report_Table(self, dct_={}, terminal_print=False, ask_when_hosts_fail=False):
        table = self.ssh.connection_report_Table(dct=dct_, terminal_print=terminal_print, ask_when_hosts_fail=ask_when_hosts_fail)
        return table
    
    def execute(self, host_dct, cmd, terminal_print='default', ask_for_confirmation=False, exit_on_fail=True, reconnect_closed_socket=True):
        """
        - Excutes a command on a remove network device
        INPUT:
            1. host_dct -> (dct) The host dictionary,  is key of the  `connected_devices_dct` attribute  (And contains information about the device including the `ssh channel` to use for the command execution )
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
            self.ssh.ask_for_confirmation(cmd=self.bcolors.OKBLUE +  cmd + self.bcolors.ENDC)
        
        # Start the execution_time couter
        start_time = time.time()
        # Execute the command
        result = self.ssh.exec(host_dct, cmd, self.vendor)
        # Calculate the execution_time
        duration = (time.time() - start_time)
        print()
        print(f"@ {host_dct['host']}")
        print("Execution Time: {} seconds".format(float("{:.2f}".format(duration))))
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
            data = f"""\n@ {host_dct['host']}
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
            if exit_on_fail:
                print()
                # Print STDERR in red color
                print(self.bcolors.FAIL + '\n'.join(result['stderr']) + self.bcolors.ENDC)
                print()
                print("> Stopped due to the previous error.")
                exit(1)
        return result

    def execute_raw(self, host_dct, cmd):
        """
        - Excutes a command on a remove network device
        INPUT:
            1. host_dct -> The host dictionary,  is key of the  `connected_devices_dct` attribute  (And contains information about the device including the `ssh channel` to use for the command execution )
            2. cmd -> The command to run on the remote device
        OUTPUT: (dictionary)
            - "stdout":    (list) "The output of the command",
            - "stderr":    (list) "The error (Syntax error are detected.)",
            - "exit_code": (int) 0 --> the command run successfully,  1 --> an error occurred
        - does NOT print to the terminal
        """
        result = self.ssh.exec(host_dct, cmd, self.vendor)
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

