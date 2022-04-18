from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Vendors import Huawei
# Create an instance of the class
task  = Terminal_Task()

cmd ='''sh vlan br
sh ip int br'''

# Loop over the ONLY authenticated devices
## task.connected_devices_dct -> Is an attribute that contains all the devices that were authenticated successfully
for host, host_dct in task.connected_devices_dct.items():
    
    # Run enable (enable password is 'cisco')
    enable = task.execute_raw(host_dct, 'enable\n' + 'cisco')
    
    # Run the following commands only if the "enable" command was executed successfully
    if enable['exit_code'] == 0: 

        # Execute a command, the output will be printed to the terminal
        task.execute(host_dct, 'sh ip int br')

        # Execute a command, the output will be printed to the terminal in JSON format
        task.execute(host_dct, cmd, terminal_print='json')
        
