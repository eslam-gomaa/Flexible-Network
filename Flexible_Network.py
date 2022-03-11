from flexible_network.ssh import SSH_connection
from flexible_network.inventory import Inventory
from flexible_network.read_cli_options import ReadCliOptions
from flexible_network.json_db import JsonDB
from flexible_network.cli import CLI
from flexible_network.Terminal_Task import Terminal_Task
from flexible_network.read_config import Config




class Flexible_Network(
    Terminal_Task,
    CLI,
    SSH_connection,
    Inventory,
    Config,
    ReadCliOptions,
    JsonDB
):
    pass

# from flexible_network.vendors.cisco import Cisco
# from flexible_network.vendors.huawei import Huawei
