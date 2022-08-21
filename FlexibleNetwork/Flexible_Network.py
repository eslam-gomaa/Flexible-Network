# The following order matters.
# from FlexibleNetwork.ssh import SSH_connection
from FlexibleNetwork.ssh_authentication import SSH_Authentication
from FlexibleNetwork.read_cli_options import ReadCliOptions
from FlexibleNetwork.read_config import Config
from FlexibleNetwork.inventory import Inventory
from FlexibleNetwork.tinydb_db import TinyDB_db
from FlexibleNetwork.cli import CLI
from FlexibleNetwork.colors import Bcolors
from FlexibleNetwork.Terminal_Task import Terminal_Task


class Flexible_Network(
    Terminal_Task,
    ReadCliOptions,
    CLI,
    # SSH_connection,
    SSH_Authentication,
    Inventory,
    Config,
    Bcolors,
    TinyDB_db
):
    pass