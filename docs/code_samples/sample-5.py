from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Vendors import Huawei
from FlexibleNetwork.Vendors import Cisco

# Create an instance of the class
task  = Terminal_Task()


# Authenticate Cisco switches group
task.authenticate(task.inventory_groups['cisco_switches'], 'orange', 'cisco', 1114)
# Set the vendor to Cisco
task.vendor = Cisco()  # The default.

for host, host_dct in task.connected_devices_dct.items():
    task.execute(host_dct, 'enable\n' + 'cisco')
    task.execute(host_dct, 'sh ip int br')
    task.backup_config(host_dct, 'test backup')

#####################   

# Authenticate Huawei switches group
task.authenticate(task.inventory_groups['huawei_switches'], 'orange', 'cisco', 1114)
# Set the vendor to Huawei
task.vendor = Huawei()

for host, host_dct in task.connected_devices_dct.items():
    # Run needed commands, this is just a test
    task.execute(host_dct, 'display ip interface brief')
    task.backup_config(host_dct, 'test backup')