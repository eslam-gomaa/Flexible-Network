from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Integrations import RocketChat_API

task = Terminal_Task()
rocket = RocketChat_API()


##  1  ## Authenticate
# task.authenticate(hosts=task.inventory_groups['all'], user='orange', password='cisco', port='1113')

##  2  ## Generate Connection Report table & save it to a variable
report = task.connection_report_Table(task.devices_dct)
## You can print the table to the terminal (The same table printed at authentication)
# print(report)

## Send the report via RocketChat to the specified user
rocket.send_message(['eslam.gomaa'], "``` {} ```".format(report))


for host, host_dct in task.connected_devices_dct.items():
    #ost_dct = task.connected_devices_dct[host]
    
    task.execute_raw(host_dct, 'enable\n' + 'cisco')
    task.execute_from_file(host_dct, 'docs/Docs/Examples/sample_config.txt', ask_for_confirmation=True, terminal_print='json')
    # task.backup_config(host_dct, 'Test config backup 1', target='local')    

