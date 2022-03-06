from Flexible_Network.ssh_authentication import SSH_Authentication
import time
import socket

class SSH_connection():
    def __init__(self):
        pass

    def connection_report(lst=[]):
        pass

    def authenticate_devices(self, hosts=[], user='orange', password='cisco', port='1113'):
        out = {}

        self.authentication = SSH_Authentication()
        for host in hosts:
            connection = self.authentication.connect(host, user, password, port)
            out[host] = connection
        return out

        
 