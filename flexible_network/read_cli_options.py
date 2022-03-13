
class ReadCliOptions:
    task_name = None
    inventory_file = None
    no_confirm_auth = False
    config_file = None
    to_validate_lst = None
    authenticate_group = None
    auth_user = None
    auth_password = None
    auth_port = None

    def __init__(self):
        self.task_name
        self.inventory_file
        self.no_confirm_auth
        self.config_file
        self.to_validate_lst
        self.authenticate_group
