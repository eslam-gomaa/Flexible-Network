from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Integrations import RocketChat_API

task = Terminal_Task()
rocket = RocketChat_API()


## * Generate Connection Report table & save it to a variable
## task.devices_dct -> is an attribute that contains all the devices (authenticated & failed to authenticate)
## Usually is used to generate reports
report = task.connection_report_Table(task.devices_dct)
## You can print the table to the terminal (The same table printed at authentication)
# print(report)

## Send the report via RocketChat to the specified user
rocket.send_message(['eslam.gomaa'], "``` {} ```".format(report))


for host, host_dct in task.connected_devices_dct.items():
    
    task.execute_raw(host_dct, 'enable\n' + 'cisco')

    # Load the commands from a file
    # ask_for_confirmation -> you need to confirm before the commands are executed
    # terminal_print='json' -> Print the output in JSON format
    task.execute_from_file(host_dct, 'docs/code_samples/sample_config.txt', ask_for_confirmation=True, terminal_print='json')

