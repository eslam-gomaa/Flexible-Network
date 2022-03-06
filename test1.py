from cmath import inf
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
hosts_dct = ssh.authenticate_devices(hosts=['90.84.41.239', '90.84.41.2'], user='orange', password='cisco', port='1113')

# Store the only connected hosts to a dict.
hosts_dct_connected = {}
for host in hosts_dct:
    if hosts_dct[host]['is_connected']:
        hosts_dct_connected[host] = hosts_dct[host]


### Another way to iterate through the only connected hosts
# for host, info in hosts_dct.items():
#     if info['is_connected']:
#         print(info)


for host, info in hosts_dct_connected.items():
    info['channel'].send(cmd + '\n' + '\n')
    time.sleep(0.5)
    output = hosts_dct['90.84.41.239']['channel'].recv(9999).decode("utf-8")
print(output)

