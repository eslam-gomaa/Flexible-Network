from tinydb import TinyDB, Query
import uuid

class TinyDB_db:
    def __init__(self):
        self.db_file = 'db.json'
        # This will create the DB file if it does NOT exist.
        self.db = TinyDB(self.db_file)
        self.tasks_table = self.db.table('tasks')
        self.backups_table = self.db.table('backups')


    def get_tasks_table_items(self):
        """
        Returns all rows of the 'tasks' table
        """
        return self.tasks_table.all()

    def insert_task(self, dct):
        """
        Insert a new task 'dictionary'  in the 'tasks' table
        """
        self.tasks_table.insert(dct)

    def update_task(self, dct, task_id):
        """
        Updates the row if exists
        """
        Task = Query()
        self.tasks_table.update(dct, Task.id == task_id)

    def upsert_task(self):
        """
        If it finds any documents matching the query, 
        they will be updated with the data from the provided document. 
        On the other hand, if no matching document is found, 
        it inserts the provided document into the table:
        """
        Task = Query()
        self.tasks_table.upsert({'name': 'ahmed', 'id': 555}, Task.id == '123')


    def search(self):
        task = Query()
        results = self.db.search(task.name == 'eslam')
        return results





# d = TinyDB_db()
# # id = uuid.uuid4()
# id = 'e9ed9557-614b-4297-b90d-9441e50087f6'
# # d.insert_task({'id': str(id)})
# print(d.update_task({'name': 'eslam'}, id))
# print(d.get_tasks_table_items())
