from Flexible_Network import Config
from Flexible_Network import ReadCliOptions


class Inventory():
    # Define 'inventory_file' as a class level attribute, so that I can update it from the cli class 
    # Need to specify the default value in the configuration file

    def __init__(self):
        # Check the input is file
        if ReadCliOptions.inventory_file is None:
            pass
            config = Config()
            self.inventory_file = config.section_general['default_inventory']
        else:
            self.inventory_file = ReadCliOptions.inventory_file

        self.inventory = {'group1': ['90.84.41.239']}

    def read_inventory(self):
        """ 
        Read the hosts into groups 
        Returns list of dicts (each dict is a list of hosts)
        """
        return self.inventory_file
