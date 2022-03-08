from Integrations.rocket_chat import RocketChat_API
# from Flexible_Network.ssh_connection import SSH_connection
from Flexible_Network.ssh_test import SSH_connection
from Flexible_Network.vendors.cisco import Cisco

ssh = SSH_connection()
rocket = RocketChat_API()
vendor = Cisco()

print(vendor.clean_output_search_keyword())
exit(1)

# Get ssh connection info from the "connection" class attribute.
# connection_info = ssh.connection
# print(connection_info)

# print(ssh.execute('sh ip int br')['stdout'])

# # Executing a command on the network device using the "execute" method.
# test_command = ssh.execute('sh ip int br')
# print(test_command['stdout'])

# msg = rocket.send_message('eslam.gomaa', test_command['stdout'])
# print(msg)


pa3_lst = ['90.84.41.239']
print("[ Testing ] Authenticating")


##  1  ## Authenticate
hosts_dct = ssh.authenticate(hosts=pa3_lst, user='orange', password='cisco', port='1113')

##  2  ## Get Connection Report
report = ssh.connection_report_Table(hosts_dct)
print(report)
# rocket_msg = rocket.send_message(['eslam.gomaa'], "``` {} ```".format(report))
# print(rocket_msg)




# Store the only connected hosts to a dict.
hosts_dct_connected = {}
for host in hosts_dct:
    if hosts_dct[host]['is_connected']:
        hosts_dct_connected[host] = hosts_dct[host]



### Another way to iterate through the only connected hosts
# for host, info in hosts_dct.items():
#     if info['is_connected']:
#         print(info)



### Test exeuting a command.

import time
cmd ='''sh ip int br
show vlan br
'''

for host, host_auth in hosts_dct_connected.items():
    channel = host_auth['channel']
    
    command1 = ssh.exec(channel, cmd)
    print(command1)

