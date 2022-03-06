import imp
from Integrations.rocket_chat import RocketChat_API
# from Flexible_Network.ssh_connection import SSH_connection
from Flexible_Network.ssh_test import SSH_connection

ssh = SSH_connection()
rocket = RocketChat_API()

# Get ssh connection info from the "connection" class attribute.
# connection_info = ssh.connection
# print(connection_info)

# print(ssh.execute('sh ip int br')['stdout'])

# # Executing a command on the network device using the "execute" method.
# test_command = ssh.execute('sh ip int br')
# print(test_command['stdout'])

# msg = rocket.send_message('eslam.gomaa', test_command['stdout'])
# print(msg)

import time

cmd ='sh vlan br'

print("* Authenticate")
a = ssh.auth()
print(a)
print()


if a['is_connected']:
    a['channel'].send(cmd + '\n' + '\n')
    time.sleep(0.5)
    output = a['channel'].recv(9999).decode("utf-8")

print(output)
