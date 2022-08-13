from tinydb import TinyDB, Query
from tinydb.operations import increment, add, set
from tabulate import tabulate
import os
from pathlib import Path
import textwrap
from FlexibleNetwork.Integrations import S3_APIs
import rich
from rich.markdown import Markdown


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

    def delete_tasks_table(self, task_id):
        """
        Delete backup from the 'backups' table
        """
        Task = Query()
        self.tasks_table.remove(Task.id == task_id)

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
            task_entry_dct = self.tasks_table.search(Task.id == task_id)[0]
            log_file = task_entry_dct['log_file']
            print()
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
            if task_entry_dct['format'] == 'markdown':
                rich.print(Markdown(file.read()))
            elif task_entry_dct['format'] == 'txt':
                print(file.read())
            exit(0)

    ### Backups Table ###
    def get_backups_table_items(self):
        """
        Returns all rows of the 'backups' table
        """
        return self.backups_table.all()

    def insert_backups_table(self, dct):
        """
        Insert a new backup 'dictionary'  in the 'backups' table
        """
        self.backups_table.insert(dct)

    def update_backups_table(self, dct, backup_id):
        """
        Updates the row if exists
        """
        Backup = Query()
        self.backups_table.update(dct, Backup.id == backup_id)

    def delete_backups_table(self, backup_id):
        """
        Delete backup from the 'backups' table
        """
        Backup = Query()
        self.backups_table.remove(Backup.id == backup_id)

    def increment_key_backups_table(self, key, backup_id):
        """
        Updates the row if exists
        """
        Task = Query()
        self.backups_table.update(increment(key), Task.id == backup_id)

    # def return_backup2(self, backup_id, print=True):
    #     try:
    #         Backup = Query()
    #         target = self.backups_table.search(Backup.id == backup_id)[0]['target']
    #         location = self.backups_table.search(Backup.id == backup_id)[0]['location']
    #         if target == 'local':
    #             if not os.path.isfile(location):
    #                 print(f"ERROR -- Could NOT find Backup file [ {location} ]")
    #                 exit(1)
    #             with open(location, 'r') as file:
    #                 print(file.read())
    #                 exit(0)
    #         if target == 's3':
    #             # get the config from S3
    #             s3 = S3_APIs()
    #             get_backup_file = s3.get_object(bucket=location[0], file_name=location[1])
    #             if get_backup_file['success']:
    #                 print(get_backup_file['output'])
    #                 # print(f"[ Bucket: {location[0]}, Key: {location[1]} ]")
    #                 exit(0)
    #             else:
    #                 raise SystemExit(f"ERROR -- Failed to get the backup form S3 [ Bucket: {location[0]}, Key: {location[1]} ]\n> {get_backup_file['fail_reason']}")
    #     except IndexError:
    #         print("ERROR -- Could NOT find the backup >> Invalid backup ID")
    #         exit(1)


    def return_backup(self, backup_id):
        class Output:
            def __init__(self):
                self.exit_code = 1
                self.stderr = ""
                self.stdout = ""
                self.target = ""
                self.location = ""
                self.text = ""
        output = Output()

        try:
            Backup = Query()
            target = self.backups_table.search(Backup.id == backup_id)[0]['target']
            output.target = target
            location = self.backups_table.search(Backup.id == backup_id)[0]['location']
            output.location = location

            # If the backup was faild, no need to try to get it.
            if not self.backups_table.search(Backup.id == backup_id)[0]['success']:
                output.exit_code = 1
                output.stderr = "There was an Error while taking this backup !"
                output.text = "\n".join(self.backups_table.search(Backup.id == backup_id)[0]['failed_reason'])
                output.stdout = "failed"
                return output

            if target == 'local':
                if not os.path.isfile(location):
                    output.stderr = f"Could NOT find Backup file [ {location} ]"
                    output.exit_code = 1
                try:
                    with open(location, 'r') as file:
                        output.text = file.read()
                        output.exit_code = 0
                        output.stdout = "success"
                except FileNotFoundError  as e:
                    output.stderr = f"Backup file is not found, {e}"
                    output.exit_code = 1

            if target == 's3':
                # get the config from S3
                s3 = S3_APIs()
                get_backup_file = s3.get_object(bucket=location[0], file_name=location[1])
                if get_backup_file['success']:
                    output.text = get_backup_file['output']
                    # print(f"[ Bucket: {location[0]}, Key: {location[1]} ]")
                    # exit(0)
                else:
                    output.stderr = f"Failed to get the backup form S3 [ Bucket: {location[0]}, Key: {location[1]} ]\n> {get_backup_file['fail_reason']}"
                    output.exit_code = 1
        except IndexError:
            output.exit_code = 1
            output.stderr = "Could NOT find the backup >> Invalid backup ID"
            # print("ERROR -- Could NOT find the backup >> Invalid backup ID")
            # exit(1)
        return output





d = TinyDB_db()
# # id = uuid.uuid4()
# id = 'e9ed9557-614b-4297-b90d-9441e50087f6'
# # d.insert_task({'id': str(id)})
# print(d.update_task({'name': 'eslam'}, id))
print()
# print(d.get_backups_table_items())
