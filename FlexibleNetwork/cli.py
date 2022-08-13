import argparse
from FlexibleNetwork.Flexible_Network import ReadCliOptions
import sys


class CLI:
    def __init__(self):
        self.parser = None

    def argparse(self):
        parser = argparse.ArgumentParser(description='A Python tool that to automate network devices with much flexibility & lots of integrations')
        
        parser.add_argument('-n', '--name', type=str,required=False, metavar='', help='The Task Name')
        parser.add_argument('-i', '--inventory', type=str, required=False, metavar='', help='The inventory file')
        parser.add_argument('-V', '--validate-integration', nargs='+',choices=['cyberArk', 'rocketChat', 's3'], help='Test API Integrations')
        parser.add_argument('-x', '--no-confirm-auth', action='store_true', help='Skip Asking for confirmation if failed to connect to some deivces')
        parser.add_argument('-c', '--config', type=str, required=False, metavar='', help='The path of configuration file')
        parser.add_argument('-g', '--authenticate-group', type=str, required=False, metavar='', help='Authenticate an inventory group')
        parser.add_argument('-u', '--user', type=str, required=False, metavar='', help='The user to authenticate the group')
        parser.add_argument('-p', '--password', type=str, required=False, metavar='', help='The password to authenticate the group')
        parser.add_argument('-P', '--port', type=int, required=False, default=22, metavar='', help='The port to connect to the group')
        parser.add_argument('-f', '--file', type=str, required=False, metavar='', help='YAML manifest file  .yaml OR .yml')
        parser.add_argument('-d', '--debug', action='store_true', help='Print debug outputs')

        parser.add_argument('-b', '--backup', action='store_true', help='Deal with Backups')
        parser.add_argument('-gb', '--get-backup', type=str,help='Returns the configuuration backup')
        parser.add_argument('-t', '--task', action='store_true', help='Deal with Lists')
        parser.add_argument('-gl', '--get-log', type=str, help='Returns the task log')
        parser.add_argument('-A', '--all', action='store_true', help='List ALL backups or tasks, default: last 15')
        parser.add_argument('-D', '--delete', type=str, default="", help='Delete a task or backup by id')

        parser.add_argument('-l', '--list', action='store_true', help='List tasks Or backups')
        parser.add_argument('-C', '--check', action='store_true', help='Validates the YAML file for errors')
        
        results = parser.parse_args()
        self.parser = parser

        # If --name & --task & --backup are specified
        if (results.backup) and (results.task) and (results.name):
            print("> You can NOT specify --name with --task or --backup")
            print("\n\t\t\t* * *\n")
            print(parser.print_help(sys.stderr))
            exit(1)
        # If --name & (--task OR --backup) are specified
        elif (results.backup or results.task) and (results.name):
            print("> You can NOT specify --name with --task or --backup")
            print("\t\t\t* * *\n")
            print(parser.print_help(sys.stderr))
            exit(1)
        # If --task and --backup are specified
        elif (results.backup) and (results.task):
            print("> You can NOT specify --task & --backup together\n")
            print("\t\t\t* * *\n")
            print(parser.print_help(sys.stderr))
            exit(1)
        
        # If nothting from the main options are specified
        # Should add validate_integration as well as a main option.
        # elif (not results.backup and not results.task and not results.name and not results.validate_integration):
        #     print("> Supported options:")
        #     print("  --name                     Run a new task")
        #     print("  --task                     List tasks or get task log")
        #     print("  --backup                   List backups or get a backup")
        #     print("  --validate-integration     Validate the integrations with external apis")
        #     print("\n\t\t\t* * *\n")
        #     print(parser.print_help(sys.stderr))
        #     exit(1)

        # If only --task is specified
        elif (results.task) and not (results.list or results.get_log or results.delete):
            print("> Supported options:")
            print("  --list                     List all tasks")
            print("  --get-log                  Return task log")
            print("  --delete                   Delete task")
            print("\n\t\t\t* * *\n")
            print(parser.print_help(sys.stderr))
            exit(1)

        # If only --backup is specified
        elif (results.backup) and not (results.list or results.get_backup or results.delete):
            print("> Supported options:")
            print("  --list                     List all backups")
            print("  --get-backup               Return backup")
            print("  --delete                   Delete backup")
            print("\n\t\t\t* * *\n")
            print(parser.print_help(sys.stderr))
            exit(1)



        # if --task --list
        if (results.task and results.list):
            ReadCliOptions.list_tasks = True

        if results.all:
            ReadCliOptions.list_all = results.all

        if (results.task and results.delete):
            ReadCliOptions.delete_task = True
            ReadCliOptions.delete = results.delete

        if (results.backup and results.delete):
            ReadCliOptions.delete_backup = True
            ReadCliOptions.delete = results.delete

        if (results.task and (results.get_log is not None)):
            ReadCliOptions.get_log = results.get_log

        if (results.backup and results.list):
            ReadCliOptions.list_backups = True

        if (results.backup and (results.get_backup is not None)):
            ReadCliOptions.get_backup = results.get_backup

        if results.inventory is not None:
            ReadCliOptions.inventory_file = results.inventory

        if results.debug:
            ReadCliOptions.debug = results.debug

        if results.file:
            ReadCliOptions.yaml_file = results.file
        
        if results.check:
            ReadCliOptions.yaml_file_check = results.check

        if results.name is not None:
            ReadCliOptions.task_name = results.name
        
        if results.validate_integration is not None:
            # Convert the list to a set to remove the duplicates
            ReadCliOptions.to_validate_lst = set(results.validate_integration)

        if results.no_confirm_auth:
            ReadCliOptions.no_confirm_auth = True
        
        if results.config is not None:
            ReadCliOptions.config_file = results.config

        if results.authenticate_group is not None:
            if (results.user is None) or (results.password is None):
                print("ERROR -- Required for --authenticate-group")
                print("> --user and --password should be provided")
                exit(1)
            ReadCliOptions.authenticate_group = results.authenticate_group
            ReadCliOptions.auth_user = results.user
            ReadCliOptions.auth_password = results.password
            ReadCliOptions.auth_port = results.port
            
            


