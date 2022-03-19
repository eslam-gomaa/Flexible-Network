from distutils.command.config import config
from flexible_network.Vendors import Cisco
from Flexible_Network import ReadCliOptions
from Flexible_Network import CLI
from Flexible_Network import Config
from Flexible_Network import Inventory
from Flexible_Network import SSH_connection
from Integrations import RocketChat_API
from tabulate import tabulate
import uuid
from Flexible_Network import TinyDB_db
from Flexible_Network import Bcolors
import json
from pygments import highlight, lexers, formatters
from datetime import datetime
import random
from pathlib import Path
import time


class Terminal_Task:
    task_name = None # Should be updated from a cli option. --task

    def __init__(self):
        # Initialize the "CLI" class so that it read the cli options 
        cli = CLI()
        cli.argparse()
        # Initialize the "Config" class so that it checks the config file at the begining. 
        config = Config()
        inventory = Inventory()
        self.ssh = SSH_connection()
        self.validate_integrations()
        self.db = TinyDB_db()
        self.bcolors = Bcolors()
        self.local_db_dir = '.db'
        self.log_and_backup_dir = self.local_db_dir +  '/' + datetime.today().strftime('%d-%m-%Y')


        if ReadCliOptions.list_tasks:
            # print("list")
            print(self.db.list_all_tasks())
            exit(0)

        if ReadCliOptions.list_backups:
            # print("list")
            print(self.db.list_all_backups())
            exit(0)


        # Gernate the task id
        self.task_id = str(uuid.uuid4())
        self.log_file = self.log_and_backup_dir + '/' + self.task_id + '.txt'
        print(self.log_file)
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
                                   'date': date, 
                                   'time': time,
                                   'full_devices_n': 0,
                                   'authenticated_devices_n': 0
                                   })


        # Should get the vendor based on conditions
        self.vendor = Cisco() # Default vendor class should exist in the config
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


            if 'rocketChat' in ReadCliOptions.to_validate_lst:
                rocket = RocketChat_API() 
                out = {}
                out['success'] = False
                out['comment'] = ""
                try:
                    rocket.auth_raw()
                    out['success'] = True
                    out['comment'] = "Works !"

                except:
                    out['comment'] = 'Authentication Failed'
                if out['success']:
                    status = '🟢'
                else:
                    status = '🔴'
                row = ['rocketChat', status, out['comment']]
                table.append(row)
            out = tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)
            print(out)
            exit(1)

    def authenticate(self, hosts=[], user='orange', password='cisco', port='1113', terminal_print=True):
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
            self.db.update_tasks_table({'log_file': self.log_file}, self.task_id)
        else:
            self.db.update_tasks_table({'log_file': None}, self.task_id)



    def update_log_file(self, data):
        with open(self.log_file, 'a') as file:
            file.write(data)

    def connection_report_Table(self, dct_={}, terminal_print=False, ask_when_hosts_fail=False):
        table = self.ssh.connection_report_Table(dct=dct_, terminal_print=terminal_print, ask_when_hosts_fail=ask_when_hosts_fail)
        return table
    
    def execute(self, host_dct, cmd, terminal_print='default', ask_for_confirmation=False, exit_on_fail=True):
        """
        - Excutes a command on a remove network device
        - Returns a dictionary:
        {
            "stdout": "The output of the command",
            "stderr": "The error (Syntax error are detected.)",
            "exit_code":  0 --> the command run successfully,  1 --> an error occurred
        }
        - Options:
            - terminal_print: print the ouput || error to the terminal
            - ask_for_confirmation: ask for confirmation before executing a command, default: False
            - exit_on_fail: exit the script with code 1 if the command executed with errors  default: True
        """
        date_time = datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
        start_time = time.time()
        if ask_for_confirmation:
            self.ssh.ask_for_confirmation(cmd=self.bcolors.OKBLUE +  cmd + self.bcolors.ENDC)
        result = self.ssh.exec(host_dct['channel'], cmd)
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
            data = f"""Time: {date_time}
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
                print("Stopped due to the previous error.")
                exit(1)
        return result

    def execute_raw(self, host_dct, cmd):
        """
        - Excutes a command on a remove network device
        - Returns a dictionary:
        {
            "stdout": "The output of the command",
            "stderr": "The error (Syntax error are detected.)",
            "exit_code":  0 --> the command run successfully,  1 --> an error occurred
        }
        - does NOT print to the terminal
        """
        result = self.ssh.exec(host_dct['channel'], cmd)
        return result

    def backup_config(self, host_dct, comment, target='local'):
        """
        Take full configurations backup of the device
        """
        result = self.ssh.backup_config(host_dct['channel'], comment, target)

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
        if result['exit_code'] == 0:
            # Clean the backup output [ Remove the backup commands ]
            backup_output = '\n'.join(result['stdout'])
            for c in self.vendor.backup_command.split("\n"):
                import re
                backup_output = backup_output.replace(c.lstrip().strip(), '')
                backup_output = backup_output.strip()

            backup_file = host_dct['host'] + '-{}.txt'.format(uuid.uuid4().hex.upper()[0:10])

            
            # Update Log file
            date_time = datetime.today().strftime('%d-%m-%Y_%H-%M-%S')
            start_time = time.time()
            duration = (time.time() - start_time)
            if self.log_output:
                output = '\n'.join(result['stdout'])
                error = '\n'.join(result['stderr'])
                data = f"""Time: {date_time}
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
                # Create a temp_file and save the backup to it
                save_backup_locally(b_dir='/tmp')
                # Upload the backup to s3
                #backup stored here
                print('/tmp/' + backup_file)

                # Remove the temp backup
    

        # Update the backup to the task table .. Add the backup ID to the 
        self.db.append_backups_ids_tasks_table('backups_ids', self.backup_id, self.task_id)
        # Increament the backups number in the task by 1
        self.db.increment_key_tasks_table('n_of_backups', self.task_id)
        print("\n@ {}".format(host_dct['host']))
        if result['exit_code'] == 0:
            print("> backup taken successfully > [ {} ]".format(comment))
            self.db.update_backups_table({'success': True}, self.backup_id)
        else:
            print("ERROR -- Failed to backup config > [ {} ]".format(comment))
            # self.db.update_backups_table({'success': False}, self.backup_id)
            self.db.update_backups_table({'failed_reason': result['stderr']}, self.backup_id)
            print(self.bcolors.FAIL + '\n'.join(result['stderr']) + self.bcolors.ENDC)

