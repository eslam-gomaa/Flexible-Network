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
# rocket.send_message(['eslam.gomaa'], f"``` {report} ```")


### Test exeuting a command.

cmd ='''
    sh vlan br
    conf t        
     '''


for host in task.connected_devices_dct:     
    host_dct = task.connected_devices_dct[host]
    
    enable = task.execute(host_dct, 'enable\n' + 'cisco', ask_for_confirmation=True)
    task.execute(host_dct, cmd, terminal_print='json')


