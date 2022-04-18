from FlexibleNetwork.Flexible_Network import Terminal_Task

# Create an instance of the class
task  = Terminal_Task()


cmd ='''sh vlan br
sh ip int br'''

# Loop over the ONLY authenticated devices
for host, host_dct in task.connected_devices_dct.items():
    
    # Run enable (enable password is 'cisco')
    enable = task.execute_raw(host_dct, 'enable\n' + 'cisco')

    # Execute a command, the output will be printed to the terminal
    task.execute(host_dct, 'sh ip int br')

    # Backup config and store the backup to S3 (In this example "Openstack object storage")
    task.backup_config(host_dct, 'Testing S3 integrations', target='s3')    

