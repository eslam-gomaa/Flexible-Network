from base64 import encode
from cmath import inf
from Flexible_Network.ssh_authentication import SSH_Authentication
import time
import socket
from tabulate import tabulate
import textwrap
import emoji

class SSH_connection():
    def __init__(self):
        pass

    def authenticate_devices(self, hosts=[], user='orange', password='cisco', port='1113'):
        """
        Autenticates a List of devices and returns a dictionary of dictionaries,
        * The key of each nested dict is the host IP and the value is the connection & authentication information.
        """
        out = {}
        self.authentication = SSH_Authentication()
        for host in hosts:
            connection = self.authentication.connect(host, user, password, port)
            out[host] = connection
        return out

    def connection_report(self, dct={}):
        """
        Takes an dict generated from the "authenticate_devices" Method
        And prints them in a an organized table
        """
        table = [['Host', 'Connection Status', 'Comment', 'N of tries', 'Max Retries', 'Time to connect in seconds', 'Fail Reason']]
        tabulate.WIDE_CHARS_MODE = False
        for host, info in dct.items():
            
            if info['is_connected']:
                connection_status = "🟢"
                comment = "connected"
            else:
                connection_status = "🔴"
                comment = "Fail to connect"
            fail_reason = "\n".join(textwrap.wrap(info['Fail_Reason'], width=26, replace_whitespace=False))
            
            row = [host, connection_status, comment, info['tries'], info['max_tries'], info['time_to_connect_seconds'], fail_reason]
            table.append(row)
            
        return tabulate(table, headers='keys', tablefmt='grid', showindex=False)

       
        
 