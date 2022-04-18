from FlexibleNetwork.Flexible_Network import Terminal_Task
# Create an instance of the class
task  = Terminal_Task()

cmd ='''
enable
cisco
conf t
vlan 113
name Testing114
exit
exit
show vlan br 
'''

# Loop over the ONLY authenticated devices
## task.connected_devices_dct -> Is an attribute that contains all the devices that were authenticated successfully
for host, host_dct in task.connected_devices_dct.items():
    
    task.execute(host_dct, cmd, ask_for_confirmation=True, terminal_print='json')


# End