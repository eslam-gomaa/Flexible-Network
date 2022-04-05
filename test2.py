from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Integrations import RocketChat_API
# from FlexibleNetwork.Integrations import Cyberark_APIs_v2


task = Terminal_Task()
rocket = RocketChat_API()
# cyberark = Cyberark_APIs_v2()

# print(cyberark.search_accounts(search='egomaa'))

##  1  ## Authenticate
task.authenticate(hosts=task.inventory_groups['switches2'], user='orange', password='cisco', port='1113')

# print(task.devices_dct)

##  2  ## Get Connection Report
# report = task.connection_report_Table(task.devices_dct)
# print(report)
# rocket.send_message(['eslam.gomaa'], f"``` {report} ```")


### Test exeuting a command.

# exit(0)

cmd ='''
    sh vlan br       
     '''


for host in task.connected_devices_dct:     
    host_dct = task.connected_devices_dct[host]
    
    task.execute_raw(host_dct, 'enable\ncisco')
    task.execute(host_dct, cmd, terminal_print='json', ask_for_confirmation=True)
    task.execute(host_dct, 'sh ip int br')

