import argparse
from Flexible_Network import Inventory
# from Flexible_Network import Terminal_Task
from Flexible_Network import ReadCliOptions



class CLI:
    def __init__(self):
        pass

    def argparse(self):
        parser = argparse.ArgumentParser(description='A Python tool that to automate network devices with much flexibility & lots of integrations')
        parser.add_argument('-n', '--name', type=str, required=True, metavar='', help='The Task Name')
        parser.add_argument('-i', '--inventory', type=str, required=False, metavar='', help='The inventory file')
        # parser.add_argument('-r', '--validate-RocketChat-api', action='store_true', help='Test RocketChat Integration')
        # parser.add_argument('-c', '--validate-CyberArk-api', action='store_true', help='Test RocketChat Integration')
        parser.add_argument('-V', '--validate-integration', nargs='+',choices=['cyberArk', 'rocketChat'] , required=False, metavar='', help='Test API Integrations')
        parser.add_argument('-o', '--no-confirm-auth', action='store_true', help='Skip Asking for confirmation if failed to connect to some deivces')


        results = parser.parse_args()
        if results.inventory is not None:
            # Inventory.inventory_file = results.inventory
            ReadCliOptions.inventory_file = results.inventory
        if results.name is not None:
            ReadCliOptions.task_name = results.name
        
        if results.validate_integration is not None:
            print(results.validate_integration)
        # need to remove duplicates
        # loop over the list, ex. if rocket chat -> call method validate_rocket_chat.

        if results.no_confirm_auth:
            ReadCliOptions.no_confirm_auth = True
