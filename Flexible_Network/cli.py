# import sys
# import os
import argparse
from Flexible_Network.inventory import Inventory
from Flexible_Network import Terminal_Task
from Flexible_Network.read_config import ReadCliOptions



class CLI:
    def __init__(self):
        pass

    def argparse(self):
        parser = argparse.ArgumentParser(description='A Python tool that to automate network devices with much flexibility & lots of integrations')
        parser.add_argument('-n', '--name', type=str, required=True, metavar='', help='The Task Name')
        parser.add_argument('-i', '--inventory', type=str, required=False, metavar='', help='The inventory file')

        results = parser.parse_args()
        if results.inventory is not None:
            # Inventory.inventory_file = results.inventory
            ReadCliOptions.inventory_file = results.inventory
        if results.name is not None:
            ReadCliOptions.task_name = results.name
