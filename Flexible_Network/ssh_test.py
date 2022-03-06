from Flexible_Network.ssh_authentication import SSH_Authentication
import time
import socket

class SSH_connection():
    def __init__(self):
        pass

    def connection_report(lst=[]):
        pass

    def auth(self, host='90.84.41.239', user='orange', password='cisco', port='1113'):
        self.authentication = SSH_Authentication()
        self.connection = self.authentication.connect(host, user, password, port)
        return self.connection
