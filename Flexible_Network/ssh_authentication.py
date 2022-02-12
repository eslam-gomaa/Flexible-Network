import paramiko
import time
import socket


class SSH_Authentication():
    def __init__(self):
        self.ssh = None
        self.info = {}
        self.info['is_connected'] = False
        self.info['tries'] = 0
        # self.info['channel'] = None
        self.info['Fail_Reason'] = ""

    def connect(self, host, user, password, port=22, ssh_timeout=15, allow_agent=True, max_tries=5):
        self.info['host'] = host
        self.info['max_tries'] = max_tries
        self.info['ssh_timeout'] = ssh_timeout

        while  self.info['tries'] < max_tries:
            self.info['tries'] += 1
            try:
                self.ssh = paramiko.SSHClient()
                
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(host, port, user, password, timeout=ssh_timeout,
                                    allow_agent=allow_agent, look_for_keys=False)
                channel = self.ssh.invoke_shell()
                self.info['is_connected'] = True

                output = channel.recv(9999)
                channel.send_ready()
                time.sleep(1)
                break
            except paramiko.AuthenticationException as e:
                self.info['Fail_Reason'] = "Authentication failed >> {}".format(e)
                break
            except socket.gaierror as e:
                self.info['Fail_Reason'] = "Could not resolve hostname {} Name or service not known >> {}".format(host, e)
                break
            except (ConnectionResetError, paramiko.ssh_exception.SSHException) as e:
                self.info['Fail_Reason'] = "Connection reset by peer >> {}".format(host, e)
                # Do NOT work as expected
                # https://github.com/napalm-automation/napalm/issues/963
                # Faced when setting the port to 111
                break
            except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.SSHException, socket.error)  as e:
                time.sleep(0.4)
                self.info['Fail_Reason'] = "NOT able to establish ssh connection with {} on port {} >> {}".format(host, port, e)
                if self.info['tries'] == max_tries:
                    break
        data = {}
        data['ssh_session'] = self.ssh
        data['data'] = self.info
        return data




# connection = SSH_Authentication()
# connect = connection.connect(host='90.84.41.239', user='orange', password='cisco1', port='1114')
# print(connect)
# import json
# print(json.dumps(connect['data'], indent=4, sort_keys=True, ensure_ascii=False))
