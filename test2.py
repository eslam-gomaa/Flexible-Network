from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Integrations import RocketChat_API
# from FlexibleNetwork.Integrations import Cyberark_APIs_v2


task = Terminal_Task()
rocket = RocketChat_API()
# cyberark = Cyberark_APIs_v2()

# print(cyberark.search_accounts(search='egomaa'))

##  1  ## Authenticate
# task.authenticate(hosts=task.inventory_groups['all'], user='orange', password='cisco', port='1113')

##  2  ## Get Connection Report
report = task.connection_report_Table(task.devices_dct)
# print(report)
rocket.send_message(['eslam.gomaa'], "``` {} ```".format(report))


### Test exeuting a command.

cmd ='''sh vlan br716
sh ip int br'''


for host in task.connected_devices_dct:
    host_dct = task.connected_devices_dct[host]
    
    task.execute_raw(host_dct, 'enable\n' + 'cisco')
    task.execute(host_dct, cmd, terminal_print='default')
    task.execute(host_dct, cmd, terminal_print='json')
    task.backup_config(host_dct, 'Testing with Dakhli', target='local')    
    task.backup_config(host_dct, 'before important update', target='local')    

