from tinydb import TinyDB, Query
from tinydb.operations import increment, add, set
from tabulate import tabulate
import os
from pathlib import Path



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

    def list_all_tasks(self, wide=False):
        table = [['id', 'name', 'comment', 'n_of_backups', 'date', 'time']]
        if wide:
            table = [['id', 'name', 'comment', 'n_of_backups', 'date', 'time', 'full_devices_n', 'authenticated_devices_n']]
        all_tasks_lst =  self.tasks_table.all()
        for task in all_tasks_lst:
            row = [task['id'], task['name'], task['comment'], task['n_of_backups'], task['date'], task['time']]
            if wide:
                row = [task['id'], task['name'], task['comment'], task['n_of_backups'], task['date'], task['time'], task['full_devices_n'], task['authenticated_devices_n']]
            table.append(row)
        out = tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)
        return out

    def list_all_backups(self, wide=False):
        table = [['id', 'comment', 'host', 'target', 'status','date', 'time']]
        all_backups_lst =  self.backups_table.all()
        for task in all_backups_lst:
            if task['success']:
                status = '🟢 success'
            else:
                status = '🔴 failed'
            row = [task['id'], task['comment'], task['host'], task['target'], status, task['date'], task['time']]
            table.append(row)
        out = tabulate(table, headers='firstrow', tablefmt='grid', showindex=False)
        return out



    def search(self, task_id):
        Task = Query()
        # results = self.tasks_table.search(Task.id== task_id)[0]['backups_ids']
        # return results





d = TinyDB_db()
# # id = uuid.uuid4()
# id = 'e9ed9557-614b-4297-b90d-9441e50087f6'
# # d.insert_task({'id': str(id)})
# print(d.update_task({'name': 'eslam'}, id))
print()
# print(d.get_backups_table_items())
