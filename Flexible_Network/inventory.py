# from Flexible_Network.cli import CLI
# cli = CLI()

class Inventory():
    # Define 'inventory_file' as a class level attribute, so that I can update it from the cli class 
    inventory_file = '/etc/...' # Need to specify the default value in the configuration file
    
    # @classmethod
    def __init__(self):
        self.inventory_file

        # Check the input is file


    def read_inventory(self):
        """ 
        Read the hosts into groups 
        Returns list of dicts (each dict is a list of hosts)
        """
        return self.inventory_file
