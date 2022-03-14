from distutils.command.config import config
from flexible_network.Vendors import Cisco
from Flexible_Network import ReadCliOptions
from Flexible_Network import CLI
from Flexible_Network import Config
from Flexible_Network import Inventory
from Flexible_Network import SSH_connection
from Integrations import RocketChat_API
from tabulate import tabulate


class Terminal_Task:
    task_name = None # Should be updated from a cli option. --task

    def __init__(self):
        # Initialize the "CLI" class so that it read the cli options 
        cli = CLI()
        cli.argparse()
        # Initialize the "Config" class so that it checks the config file at the begining. 
        config = Config()
        # 
        inventory = Inventory()
        self.ssh = SSH_connection()
        self.validate_integrations()

        ## Attributes ##
        self.vendor = Cisco() # Default vendor class should exist in the config
        self.task_name = ReadCliOptions.task_name
        # Read all inventory sections
        # self.inventory = inventory.read_inventory()
        self.inventory_groups = inventory.read_inventory()
        self.devices_dct = {}
        self.connected_devices_dct = {}
        self.connected_devices_number = 0
        self.connection_failed_devices_number = 0
        if ReadCliOptions.authenticate_group:
            # Get the IPs of the section to the 'self.inventory' attribute
            self.inventory = inventory.get_section(ReadCliOptions.authenticate_group)
            # Stop if the choosen group is empty
            if not self.inventory:
                print("\n> The choosen group [ {} ] has no hosts .. No need to continue.".format(ReadCliOptions.authenticate_group))
                exit(1)

            # If the section not found the 'get_section' method will return None
            # Hence the script will exit with code 1
            if self.inventory is None:
                print("\nERROR -- Inventory section [ {} ] does NOT exist !".format(ReadCliOptions.authenticate_group))
                exit(1)
            # Read the user, password, port 
            self.user = ReadCliOptions.auth_user
            self.password = ReadCliOptions.auth_password
            # Default port is 22 if not specified in the CLI
            self.port = ReadCliOptions.auth_port
            # Authenticate the choosen group
            self.authenticate(hosts=self.inventory, user=self.user, password=self.password, port=self.port)
            
    def validate_integrations(self):
        if ReadCliOptions.to_validate_lst is not None:
            """
            Validate RocketChat Authentication.
            """
            print("\n> Validating Integration")
            table = [['Integration', 'Status', 'Comment']]
            tabulate.WIDE_CHARS_MODE = False


            if 'rocketChat' in ReadCliOptions.to_validate_lst:
                rocket = RocketChat_API() 
                out = {}
                out['success'] = False
                out['comment'] = ""
                try:
                    rocket.auth_raw()
                    out['success'] = True
                    out['comment'] = "Works !"

                except:
                    out['comment'] = 'Authentication Failed'
                if out['success']:
                    status = '🟢'
                else:
                    status = '🔴'
                row = ['rocketChat', status, out['comment']]
                table.append(row)
            out = tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)
            print(out)
            exit(1)

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

