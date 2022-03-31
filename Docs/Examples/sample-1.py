from FlexibleNetwork.Flexible_Network import Terminal_Task


#################################
## Excute commands
## Store Backup In locally
#################################

task  = Terminal_Task()


cmd ='''sh vlan br
sh ip int br'''

## Execute commands & take backups
for host in task.connected_devices_dct: 
    host_dct = task.connected_devices_dct[host]
    
    enable = task.execute_raw(host_dct, 'enable\n' + 'cisco')

    if enable['exit_code'] == 0: 
        task.execute(host_dct, 'sh ip int br')
        task.execute(host_dct, cmd, terminal_print='json')
        task.backup_config(host_dct, 'Testing S3 integrations', target='local')    
