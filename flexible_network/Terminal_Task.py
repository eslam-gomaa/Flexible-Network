from Flexible_Network import CLI
from flexible_network.Vendors import Cisco
from Flexible_Network import ReadCliOptions
from Flexible_Network import Inventory
from Flexible_Network import SSH_connection
import sys
import time
import random

class Terminal_Task:
    task_name = None # Should be updated from a cli option. --task

    def __init__(self):
        cli = CLI()
        cli.argparse()
        inventory = Inventory()
        self.ssh = SSH_connection()

        ## Attributes ##
        self.vendor = Cisco() # Default vendor class should exist in the config
        self.task_name = ReadCliOptions.task_name
        self.inventory = inventory.inventory
        self.devices_dct = {}
        self.connected_devices_dct = {}
        self.connected_devices_number = 0
        self.connection_failed_devices_number = 0

    def authenticate(self, hosts=[], user='orange', password='cisco', port='1113', terminal_print=False):
        self.ssh.authenticate(hosts=hosts, user=user, password=password, port=port, terminal_print=True)
        self.devices_dct = self.ssh.devices_dct
        self.connected_devices_dct = self.ssh.connected_devices_dct
        self.connected_devices_number = self.ssh.connected_devices_number
        self.connection_failed_devices_number = self.ssh.connection_failed_devices_number
