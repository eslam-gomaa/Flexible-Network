from Flexible_Network import Terminal_Task
from Flexible_Network import Flexible_Network, SSH_connection
from flexible_network.Vendors import Cisco
from flexible_network.Vendors import Huawei
from Flexible_Network import Inventory
from Flexible_Network import ReadCliOptions
from Integrations import RocketChat_API



# from Flexible_Network.cli import CLI
# cli = CLI()
# cli.argparse()

task = Terminal_Task()

# Instanciate an instance from the SSH_connection class 
# Instanciate an instance from the SSH_connection class 
ssh = SSH_connection()
# Specify the vendor as an attribute
ssh.vendor = Cisco()
rocket = RocketChat_API()
rocket.authenticate()


# print(task.task_name)
# print(task.inventory)

# exit(1)




# print(vendor.backup_command)
# exit(1)

# Get ssh connection info from the "connection" class attribute.
# connection_info = ssh.connection
# print(connection_info)

# print(ssh.execute('sh ip int br')['stdout'])

# # Executing a command on the network device using the "execute" method.
# test_command = ssh.execute('sh ip int br')
# print(test_command['stdout'])

# msg = rocket.send_message('eslam.gomaa', test_command['stdout'])
# print(msg)


# pa3_lst = ['90.84.41.239']
# print("[ Testing ] Authenticating On Cisco Devices")


##  1  ## Authenticate
task.authenticate(hosts=task.inventory['group1'], user='orange', password='cisco', port='1113')

##  2  ## Get Connection Report
report = task.connection_report_Table(task.devices_dct)
# print(report)
rocket_msg = rocket.send_message(['eslam.gomaa'], "``` {} ```".format(report))
# print(rocket_msg)



# Store the only connected hosts to a dict.
# hosts_dct_connected = {}
# for host in hosts_dct:
#     if hosts_dct[host]['is_connected']:
#         hosts_dct_connected[host] = hosts_dct[host]



### Another way to iterate through the only connected hosts
# for host, info in hosts_dct.items():
#     if info['is_connected']:
#         print(info)



### Test exeuting a command.

import time
cmd ='''sh vlan br
'''


for host in task.connected_devices_dct:
    channel = task.connected_devices_dct[host]['channel']
    
    c = ssh.exec(channel, cmd)
    print('\n'.join(c['stdout']))
    # print(ssh.backup_config(channel, 'comment'))

# Close the ssh connection for a full group
# ssh.close(hosts_dct)

# for host in hosts_dct_connected:
#     channel = hosts_dct_connected[host]['channel']
    
#     print(ssh.exec(channel, cmd))
    # print(ssh.backup_config(channel, 'comment'))


# pa3_lst = ['90.84.41.239']
# print("[ Testing ] Authenticating On Huawei Devices")


# ##  1  ## Authenticate
# hosts_dct = ssh.authenticate(hosts=pa3_lst, user='orange', password='cisco', port='1113')

# ssh.vendor = Huawei()

# for host, host_auth in hosts_dct_connected.items():
#     channel = host_auth['channel']
    
#     print(ssh.exec(channel, cmd))
#     print(ssh.backup_config(channel, 'comment'))

