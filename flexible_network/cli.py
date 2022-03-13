import argparse
from Flexible_Network import ReadCliOptions
# from flexible_network.read_cli_options import ReadCliOptions


class CLI:
    def __init__(self):
        pass

    def argparse(self):
        parser = argparse.ArgumentParser(description='A Python tool that to automate network devices with much flexibility & lots of integrations')
        parser.add_argument('-n', '--name', type=str, required=True, metavar='', help='The Task Name')
        parser.add_argument('-i', '--inventory', type=str, required=False, metavar='', help='The inventory file')
        parser.add_argument('-V', '--validate-integration', nargs='+',choices=['cyberArk', 'rocketChat'] , required=False, metavar='', help='Test API Integrations')
        parser.add_argument('-x', '--no-confirm-auth', action='store_true', help='Skip Asking for confirmation if failed to connect to some deivces')
        parser.add_argument('-c', '--config', type=str, required=False, metavar='', help='The path of configuration file')
        parser.add_argument('-g', '--authenticate-group', type=str, required=False, metavar='', help='Authenticate an inventory group')


        results = parser.parse_args()
        if results.inventory is not None:
            ReadCliOptions.inventory_file = results.inventory

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
            ReadCliOptions.authenticate_group = results.authenticate_group

