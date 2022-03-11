import paramiko
import time
import socket
import datetime


class SSH_Authentication():
    def __init__(self):
        self.ssh = None
        self.channel = None
        self.is_connected = False
        self.Fail_Reason = ""
        self.time_to_connect_seconds = 0


    def connect(self, host, user, password, port=22, ssh_timeout=5, allow_agent=True, max_tries=3):
        """
        Need to document
        """
        self.host = host
        self.user = user
        self.password = password
        self.port = port

        time_start = datetime.datetime.now()
        self.tries = 1
        while  (self.tries <= max_tries):
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
                self.is_connected = False
                self.Fail_Reason = "Authentication failed >> {}".format(e)
                break
            except socket.gaierror as e:
                self.is_connected = False
                self.Fail_Reason = "Could NOT resolve hostname {} Name or service not known >> {}".format(host, e)
                break
            except (ConnectionResetError, paramiko.ssh_exception.SSHException) as e:
                self.is_connected = False
                self.Fail_Reason = "Connection reset by peer >> {}".format(host, e)
                # Do NOT work as expected
                # https://github.com/napalm-automation/napalm/issues/963
                # Raises Exceptions when setting the port to 111
                break
            except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.SSHException, socket.error)  as e:
                self.is_connected = False
                time.sleep(0.4)
                self.Fail_Reason = "NOT able to establish an ssh connection with {} on port {} >> {}".format(host, port, e)
                if self.tries == max_tries:
                    break   
            self.tries += 1
        info = {}
        info['is_connected'] = self.is_connected
        info['host'] = host
        info['max_tries'] = max_tries
        info['ssh_timeout'] = ssh_timeout
        info['ssh'] = self.ssh
        info['channel'] = self.channel

        time_end = datetime.datetime.now()
        time_taken = time_end - time_start
        info['time_to_connect_seconds'] = time_taken.seconds

        info['Fail_Reason'] = self.Fail_Reason
        info['tries'] = self.tries
        self.hosts_dct = info
        return info

    # def close(self, ssh):
    #     """
    #     Close the ssh session, ssh session is opened at the initialization of the Class
    #     """
    #     data = {}
    #     data['success'] = 'False'
    #     if self.is_connected:
    #         self.ssh.close()
    #         data['success'] = 'True'
    #     return data



# connection = SSH_Authentication()
# connect = connection.connect(host='90.84.41.239', user='orange', password='cisco', port='1113')
# print(connect)

# # import json
# # print(json.dumps(connect['data'], indent=4, sort_keys=True, ensure_ascii=False))

# print()
# print(connection.close())
