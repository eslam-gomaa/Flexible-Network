import argparse
from asyncio import tasks
from Flexible_Network import ReadCliOptions
# from flexible_network.read_cli_options import ReadCliOptions


class CLI:
    def __init__(self):
        pass

    def argparse(self):
        parser = argparse.ArgumentParser(description='A Python tool that to automate network devices with much flexibility & lots of integrations')
        parser.add_argument('-n', '--name', type=str, required=True, metavar='', help='The Task Name')
        parser.add_argument('-i', '--inventory', type=str, required=False, metavar='', help='The inventory file')
        # parser.add_argument('-V', '--validate-integration', nargs='+',choices=['cyberArk', 'rocketChat'], help='Test API Integrations')
        parser.add_argument('-x', '--no-confirm-auth', action='store_true', help='Skip Asking for confirmation if failed to connect to some deivces')
        parser.add_argument('-c', '--config', type=str, required=False, metavar='', help='The path of configuration file')
        parser.add_argument('-g', '--authenticate-group', type=str, required=False, metavar='', help='Authenticate an inventory group')
        parser.add_argument('-u', '--user', type=str, required=False, metavar='', help='The user to authenticate the group')
        parser.add_argument('-p', '--password', type=str, required=False, metavar='', help='The password to authenticate the group')
        parser.add_argument('-P', '--port', type=int, required=False, default=22, metavar='', help='The port to connect to the group')
        parser.add_argument('-l', '--tasks', action='store_true', help='List tasks')
        parser.add_argument('-b', '--backups', action='store_true', help='List backups')


        results = parser.parse_args()

        if results.tasks:
            ReadCliOptions.list_tasks = True
            
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
            
            


