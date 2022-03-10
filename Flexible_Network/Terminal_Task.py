from Flexible_Network.cli import CLI
class Terminal_Task:
    task_name = None # Should be updated from a cli option. --task
    def __init__(self):
        cli = CLI()
        cli.argparse()
    # 
