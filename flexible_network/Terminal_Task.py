from Flexible_Network import CLI
from flexible_network.Vendors import Cisco
from Flexible_Network import ReadCliOptions
from Flexible_Network import Inventory
from flexible_network.ssh_authentication import SSH_Authentication

class Terminal_Task:
    task_name = None # Should be updated from a cli option. --task

    def __init__(self):
        cli = CLI()
        cli.argparse()
        inventory = Inventory()
        ## Attributes ##
        self.vendor = Cisco() # Default vendor class should exist in the config
        self.task_name = ReadCliOptions.task_name
        self.inventory = inventory.inventory
        self.devices_dct = {}
        self.connected_devices_dct = {}

    def authenticate(self, hosts=[], user='orange', password='cisco', port='1113'):
        """
        Autenticates a List of devices and returns a dictionary of dictionaries,
        * The key of each nested dict is the host IP and the value is the connection & authentication information.
        """
        self.user = user
        self.password = password
        self.port = port
        out = {}
        self.authentication = SSH_Authentication()
        for host in hosts:
            connection = self.authentication.connect(host, user, password, port)
            out[host] = connection
        self.devices = out
        for host in self.devices:
            if self.devices[host]['is_connected']:
                self.connected_devices_dct[host] = self.devices[host]
        return out
