# The following order matters.
from flexible_network.ssh import SSH_connection
from flexible_network.read_cli_options import ReadCliOptions
from flexible_network.read_config import Config
from flexible_network.inventory import Inventory
from flexible_network.tinydb_db import TinyDB_db
from flexible_network.cli import CLI
from flexible_network.colors import Bcolors
from flexible_network.Terminal_Task import Terminal_Task




class Flexible_Network(
    Terminal_Task,
    ReadCliOptions,
    CLI,
    SSH_connection,
    Inventory,
    Config,
    Bcolors,
    TinyDB_db
):
    pass