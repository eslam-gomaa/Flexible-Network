from Flexible_Network import Terminal_Task
from Flexible_Network import Flexible_Network, SSH_connection
from flexible_network.Vendors import Cisco
from Integrations import RocketChat_API


task = Terminal_Task()
# ssh.vendor = Cisco()
rocket = RocketChat_API()
rocket.authenticate()


##  1  ## Authenticate
# task.authenticate(hosts=task.inventory, user='orange', password='cisco', port='1113')

##  2  ## Get Connection Report
report = task.connection_report_Table(task.devices_dct)
# print(report)
# rocket.send_message('eslam.gomaa', report)


### Test exeuting a command.

cmd ='''sh vlan br
sh ip int br'''


for host in task.connected_devices_dct:
    host_dct = task.connected_devices_dct[host]
    
    task.execute_raw(host_dct, 'enable\n' + 'cisco')
    task.execute(host_dct, cmd)
    task.backup_config(host_dct, 'Test config backup')    
    task.backup_config(host_dct, 'Test config backup 2')    
