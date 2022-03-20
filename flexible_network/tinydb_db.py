from tinydb import TinyDB, Query
from tinydb.operations import increment, add, set
from tabulate import tabulate
import os
from pathlib import Path
import textwrap



class TinyDB_db:
    def __init__(self):
        self.local_db_dir = '.db'
        self.db_file = 'db.json'
        # Create the DB dir
        if not os.path.isdir(self.local_db_dir):
            Path(self.local_db_dir).mkdir(parents=True, exist_ok=True)
            print(f"\n> WARNNING -- New project directory detected. \n> Created db directory: {self.local_db_dir}")

        # This will create the DB file if it does NOT exist.
        self.db = TinyDB(self.local_db_dir + '/' + self.db_file)
        ### We have the option to pretify the json file, but this will affect size & performance.
        # self.db = TinyDB(self.db_file, sort_keys=True, indent=4, separators=(',', ': '))
        self.tasks_table = self.db.table('tasks')
        self.backups_table = self.db.table('backups')


    ### Tasks Table ###
    def get_tasks_table_items(self):
        """
        Returns all rows of the 'tasks' table
        """
        return self.tasks_table.all()

    def insert_tasks_table(self, dct):
        """
        Insert a new task 'dictionary'  in the 'tasks' table
        """
        self.tasks_table.insert(dct)

    def update_tasks_table(self, dct, task_id):
        """
        Updates the row if exists
        """
        Task = Query()
        self.tasks_table.update(dct, Task.id == task_id)

    def increment_key_tasks_table(self, key, task_id):
        """
        Updates the row if exists
        """
        Task = Query()
        self.tasks_table.update(increment(key), Task.id == task_id)
    
    def append_backups_ids_tasks_table(self, key, value, task_id):
        """
        Appends 'backups_ids' key (of type list) with the new backup_id
        """
        Task = Query()
        val = self.tasks_table.search(Task.id== task_id)[0]['backups_ids']
        val.append(value)
        self.tasks_table.update(set(key, val), Task.id == task_id)

    def upsert_tasks_table(self):
        """
        If it finds any documents matching the query, 
        they will be updated with the data from the provided document. 
        On the other hand, if no matching document is found, 
        it inserts the provided document into the table:
        """
        Task = Query()
        self.tasks_table.upsert({'name': 'ahmed', 'id': 555}, Task.id == '123')

    def get_task_log(self, task_id):
        """
        Prints the task log
        """
        try:
            Task = Query()
            log_file = self.tasks_table.search(Task.id == task_id)[0]['log_file']
        except IndexError:
            print("Error -- Could NOT find the task log >> Invalid task ID")
            exit(1)
        if log_file is None:
            print("> This is an empty task >> N of authenticated devices is 0")
            exit(0)
        if not os.path.isfile(log_file):
            print(f"ERROR -- Could NOT find log file [ {log_file} ]")
            exit(1)
        with open(log_file, 'r') as file:
            print(file.read())
            exit(0)

    ### Backups Table ###
    def get_backups_table_items(self):
        """
        Returns all rows of the 'tasks' table
        """
        return self.backups_table.all()

    def insert_backups_table(self, dct):
        """
        Insert a new task 'dictionary'  in the 'tasks' table
        """
        self.backups_table.insert(dct)

    def update_backups_table(self, dct, task_id):
        """
        Updates the row if exists
        """
        Task = Query()
        self.backups_table.update(dct, Task.id == task_id)

    def increment_key_backups_table(self, key, task_id):
        """
        Updates the row if exists
        """
        Task = Query()
        self.backups_table.update(increment(key), Task.id == task_id)

    ###

    def list_all_tasks(self, wide=False):
        # The table header
        table = [['id', 'name', 'comment', 'n_of_backups', 'date', 'time']]
        if wide:
            table = [['id', 'name', 'comment', 'n_of_backups', 'date', 'time', 'full_devices_n', 'authenticated_devices_n']]
        # Get list of all the tasks from the DB
        all_tasks_lst =  self.tasks_table.all()
        for task in all_tasks_lst:
            comment = "\n".join(textwrap.wrap(task['comment'], width=30, replace_whitespace=False))
            task_name = "\n".join(textwrap.wrap(task['name'], width=26, replace_whitespace=False))
            row = [task['id'], task_name, comment, task['n_of_backups'], task['date'], task['time']]
            if wide:
                row = [task['id'], task_name, comment, task['n_of_backups'], task['date'], task['time'], task['full_devices_n'], task['authenticated_devices_n']]
            table.append(row)
        out = tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)
        return out

    def list_all_backups(self, wide=False):
        table = [['id', 'comment', 'host', 'target', 'status','date', 'time']]
        all_backups_lst =  self.backups_table.all()
        for task in all_backups_lst:
            comment = "\n".join(textwrap.wrap(task['comment'], width=30, replace_whitespace=False))
            if task['success']:
                status = '🟢 success'
            else:
                status = '🔴 failed'
            row = [task['id'], comment, task['host'], task['target'], status, task['date'], task['time']]
            table.append(row)
        out = tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)
        return out

    def return_backup(self, backup_id):
        try:
            Backup = Query()
            target = self.backups_table.search(Backup.id == backup_id)[0]['target']
            location = self.backups_table.search(Backup.id == backup_id)[0]['location']
            if target == 'local':
                if not os.path.isfile(location):
                    print(f"ERROR -- Could NOT find Backup file [ {location} ]")
                    exit(1)
                with open(location, 'r') as file:
                    print(file.read())
                    exit(0)
        except IndexError:
            print("ERROR -- Could NOT find the backup >> Invalid backup ID")
            exit(1)






d = TinyDB_db()
# # id = uuid.uuid4()
# id = 'e9ed9557-614b-4297-b90d-9441e50087f6'
# # d.insert_task({'id': str(id)})
# print(d.update_task({'name': 'eslam'}, id))
print()
# print(d.get_backups_table_items())
