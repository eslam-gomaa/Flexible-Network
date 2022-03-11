from cmath import cos
from flexible_network.ssh import SSH_connection
from flexible_network.inventory import Inventory
from flexible_network.read_config import ReadCliOptions
from flexible_network.read_config import Config
from flexible_network.json_db import JsonDB
from flexible_network.cli import CLI
from flexible_network.Terminal_Task import Terminal_Task



class Flexible_Network(
    SSH_connection,
    Inventory,
    Config,
    ReadCliOptions,
    JsonDB,
    CLI,
    Terminal_Task,
):
    pass

from flexible_network.vendors.cisco import Cisco
from flexible_network.vendors.huawei import Huawei
