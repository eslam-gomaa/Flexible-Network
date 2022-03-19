import argparse
from asyncio import tasks
from Flexible_Network import ReadCliOptions
import sys
# from flexible_network.read_cli_options import ReadCliOptions


class CLI:
    def __init__(self):
        pass

    def argparse(self):
        parser = argparse.ArgumentParser(description='A Python tool that to automate network devices with much flexibility & lots of integrations')
        parser.add_argument('-n', '--name', type=str, required=False, metavar='', help='The Task Name')
        parser.add_argument('-i', '--inventory', type=str, required=False, metavar='', help='The inventory file')
        # parser.add_argument('-V', '--validate-integration', nargs='+',choices=['cyberArk', 'rocketChat'], help='Test API Integrations')
        parser.add_argument('-x', '--no-confirm-auth', action='store_true', help='Skip Asking for confirmation if failed to connect to some deivces')
        parser.add_argument('-c', '--config', type=str, required=False, metavar='', help='The path of configuration file')
        parser.add_argument('-g', '--authenticate-group', type=str, required=False, metavar='', help='Authenticate an inventory group')
        parser.add_argument('-u', '--user', type=str, required=False, metavar='', help='The user to authenticate the group')
        parser.add_argument('-p', '--password', type=str, required=False, metavar='', help='The password to authenticate the group')
        parser.add_argument('-P', '--port', type=int, required=False, default=22, metavar='', help='The port to connect to the group')
        parser.add_argument('-k', '--list-tasks', action='store_true', help='List tasks')
        parser.add_argument('-j', '--list-backups', action='store_true', help='List backups')


        parser.add_argument('-b', '--backup', action='store_true', help='Deal with Backups')


        parser.add_argument('-t', '--task', action='store_true', help='Deal with Lists')
        parser.add_argument('-L', '--get-log', type=str, help='Returns the task log')

        parser.add_argument('-l', '--list', action='store_true', help='Deal with Lists')
        

        results = parser.parse_args()

        # If --name & --task & --backup are specified
        if (results.backup) and (results.task) and (results.name):
            print("Print Help")
            print("\t\t\t* * *\n")
            print(parser.print_help(sys.stderr))
            exit(1)
        # If --name & (--task OR --backup) are specified
        elif (results.backup or results.task) and (results.name):
            print("create new or perform operation on done ones")
            print("\t\t\t* * *\n")
            print(parser.print_help(sys.stderr))
            exit(1)
        # If --task and --backup are specified
        elif (results.backup) and (results.task):
            print("you can NOT specify --task & --backup together\n")
            print("\t\t\t* * *\n")
            print(parser.print_help(sys.stderr))
            exit(1)
            
        # elif (not results.backup) or (not results.task) or (not results.name):
        #     print("choose one of 3 options")
        #     print("\t\t\t* * *\n")
        #     print(parser.print_help(sys.stderr))
        #     exit(1)

        # If only --task is specified
        elif (results.task) and not (results.list or results.get_log):
            print("u have 2 options -> list // get_log\n")
            print("\t\t\t* * *\n")
            print(parser.print_help(sys.stderr))
            exit(1)



        # if --task --list
        if (results.task and results.list):
            ReadCliOptions.list_tasks = True

        if (results.task and (results.get_log is not None)):
            ReadCliOptions.get_log = results.get_log

        if results.list_tasks:
            ReadCliOptions.list_tasks = True
    
        if results.list_backups:
            ReadCliOptions.list_backups = True
            
        # elif results.list_backups is not None:
        #     ReadCliOptions.list_backups == True

        # if results.filter_by_date is not None:
        #     ReadCliOptions.filter_by_date = results.filter_by_date

        if results.inventory is not None:
            ReadCliOptions.inventory_file = results.inventory

        if results.name is not None:
            ReadCliOptions.task_name = results.name
        
        # if results.validate_integration is not None:
        #     # Convert the list to a set to remove the duplicates
        #     ReadCliOptions.to_validate_lst = set(results.validate_integration)

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
            
            


