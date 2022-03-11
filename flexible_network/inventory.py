# from Flexible_Network.read_config import ReadCliOptions
# from Flexible_Network import ReadCliOptions
from flexible_network.read_config import ReadCliOptions


class Inventory():
    # Define 'inventory_file' as a class level attribute, so that I can update it from the cli class 
    # Need to specify the default value in the configuration file


    # @classmethod
    def __init__(self):
        # Check the input is file
        if ReadCliOptions.inventory_file is None:
            self.inventory_file = "From config file"
        else:
            self.inventory_file = ReadCliOptions.inventory_file

        self.inventory = {'group1': ['90.84.41.239']}

    def read_inventory(self):
        """ 
        Read the hosts into groups 
        Returns list of dicts (each dict is a list of hosts)
        """
        return self.inventory_file
