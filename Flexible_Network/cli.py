# import sys
# import os
import argparse
from Flexible_Network.inventory import Inventory


class CLI:
    def __init__(self):
        self.inventory_file = None

    def argparse(self):
        parser = argparse.ArgumentParser(description='A Python tool that to automate network devices with much flexibility & lots of integrations')
        parser.add_argument('-i', '--inventory', type=str, required=False, metavar='', help='The inventory file')

        results = parser.parse_args()
        if results.inventory is not None:
            Inventory.inventory_file = results.inventory