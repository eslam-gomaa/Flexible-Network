from Flexible_Network import CLI
from flexible_network.Vendors import Cisco
from Flexible_Network import ReadCliOptions
from Flexible_Network import Inventory
from Flexible_Network import SSH_connection
# import sys
# import time
# import random

class Terminal_Task:
    task_name = None # Should be updated from a cli option. --task

    def __init__(self):
        print('from terminal task')
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

    def authenticate(self, hosts=[], user='orange', password='cisco', port='1113', terminal_print=True):
        self.ssh.authenticate(hosts=hosts, user=user, password=password, port=port, terminal_print=terminal_print)
        self.devices_dct = self.ssh.devices_dct
        self.connected_devices_dct = self.ssh.connected_devices_dct
        self.connected_devices_number = self.ssh.connected_devices_number
        self.connection_failed_devices_number = self.ssh.connection_failed_devices_number
        if terminal_print:
            if ReadCliOptions.no_confirm_auth:
                ask_when_hosts_fail_ = False
            else:
                ask_when_hosts_fail_ = True
            self.ssh.connection_report_Table(dct=self.devices_dct, terminal_print=True, ask_when_hosts_fail=ask_when_hosts_fail_)

    def connection_report_Table(self, dct_={}, terminal_print=False, ask_when_hosts_fail=False):
        table = self.ssh.connection_report_Table(dct=dct_, terminal_print=terminal_print, ask_when_hosts_fail=ask_when_hosts_fail)
        return table

