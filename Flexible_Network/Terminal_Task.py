from Flexible_Network.cli import CLI
from Flexible_Network.Vendors import Cisco
from Flexible_Network.read_config import ReadCliOptions
class Terminal_Task:
    task_name = None # Should be updated from a cli option. --task

    def __init__(self):
        cli = CLI()
        cli.argparse()
        ## Attributes ##
        self.vendor = Cisco() # Default vendor class should exist in the config
        self.task_name = ReadCliOptions.task_name

    # 
