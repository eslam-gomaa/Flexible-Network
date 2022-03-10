from Flexible_Network.ssh_authentication import SSH_Authentication
import time
import socket

class SSH_connection():
    """
    Class to connection & execute commands on network devices over ssh
    """

    def __init__(self):
        
        # Auth
        self.authentication = SSH_Authentication()
        self.connection = self.authentication.connect(host='90.84.41.239', user='orange', password='cisco', port='1113')    

    def execute(self, cmd): 
        self.cmd = cmd
        data = {}
        data['cmd'] = cmd
        try:
            if self.authentication.is_connected:
                # Test closing the connection.
                # self.authentication.ssh.close()
                self.authentication.channel.send(self.cmd + '\n' + '\n')
                time.sleep(0.5)
                self.output = self.authentication.channel.recv(9999).decode("utf-8")
                
                
                data['stdout'] = self.output
            else:
                data['stdout'] = ""

            return data
        except (OSError, socket.error) as e:
            """
            If SSH Session was interrupted
            """
            pass

    def close(self):
        if self.authentication.is_connected:
            self.authentication.close()



