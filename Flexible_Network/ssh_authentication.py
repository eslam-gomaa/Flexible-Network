import paramiko
import time
import socket
import datetime


class SSH_Authentication():
    def __init__(self):
        self.ssh = None
        self.channel = None
        self.is_connected = False
        self.tries = 0
        self.Fail_Reason = ""
        self.time_to_connect_seconds = None


    def connect(self, host, user, password, port=22, ssh_timeout=15, allow_agent=True, max_tries=5):
        self.host = host
        self.user = user
        self.password = password
        self.port = port

        time_start = datetime.datetime.now()
        while  self.tries < max_tries:
            self.tries += 1
            try:
                self.ssh = paramiko.SSHClient()
                
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(host, port, user, password, timeout=ssh_timeout,
                                    allow_agent=allow_agent, look_for_keys=False)
                self.channel = self.ssh.invoke_shell()
                self.is_connected = True

                output = self.channel.recv(9999)
                self.channel.send_ready()
                time.sleep(1)
                break
            except paramiko.AuthenticationException as e:
                self.Fail_Reason = "Authentication failed >> {}".format(e)
                break
            except socket.gaierror as e:
                self.Fail_Reason = "Could not resolve hostname {} Name or service not known >> {}".format(host, e)
                break
            except (ConnectionResetError, paramiko.ssh_exception.SSHException) as e:
                self.Fail_Reason = "Connection reset by peer >> {}".format(host, e)
                # Do NOT work as expected
                # https://github.com/napalm-automation/napalm/issues/963
                # Raises Exceptions when setting the port to 111
                break
            except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.SSHException, socket.error)  as e:
                time.sleep(0.4)
                self.Fail_Reason = "NOT able to establish ssh connection with {} on port {} >> {}".format(host, port, e)
                if self.tries == max_tries:
                    break
        info = {}
        info['is_connected'] = self.is_connected
        info['host'] = host
        info['max_tries'] = max_tries
        info['ssh_timeout'] = ssh_timeout

        time_end = datetime.datetime.now()
        time_taken = time_end - time_start
        info['time_to_connect_seconds'] = time_taken.seconds

        info['Fail_Reason'] = self.Fail_Reason
        info['tries'] = self.tries
        return info

    def close(self):
        """
        Close the ssh session, ssh session is opened at the initialization of the Class
        """
        data = {}
        data['success'] = 'False'
        if info['is_connected']:
            try:
                self.ssh.close()
                data['success'] = 'True'
            except:
                pass
        return data



# connection = SSH_Authentication()
# connect = connection.connect(host='90.84.41.239', user='orange', password='cisco', port='1113')
# print(connect)

# # import json
# # print(json.dumps(connect['data'], indent=4, sort_keys=True, ensure_ascii=False))

# print()
# print(connection.close())
