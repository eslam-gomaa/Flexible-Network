
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
    filter_by_date = None    
    get_log = False
    get_backup = False

    delete = ""
    list_all = False
    list_tasks = False
    list_backups = False
    delete_task = False
    delete_backup = False

    yaml_file = None
    yaml_file_check = False

    debug = False

    def __init__(self):
        pass