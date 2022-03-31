from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Integrations import RocketChat_API
# from FlexibleNetwork.Integrations import Cyberark_APIs_v2

#################################
## Send connect report on RocketChat
## Store Backup In S3
#################################

task  = Terminal_Task()
rocket = RocketChat_API()

## Get Connection Report
report = task.connection_report_Table(task.devices_dct)

## Send the report to RocketChat
rocket.send_message(['eslam.gomaa'], f"``` {report} ```")

## Execute commands & take backups
for host in task.connected_devices_dct: 
    host_dct = task.connected_devices_dct[host]
    
    enable = task.execute_raw(host_dct, 'enable\n' + 'cisco')
    if enable['exit_code'] == 0: 
        task.execute(host_dct, 'sh ip int br')
        task.backup_config(host_dct, 'Testing S3 integrations', target='s3')    
