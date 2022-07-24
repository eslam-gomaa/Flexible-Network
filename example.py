import rich
from numpy import rint
from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Flexible_Network import ReadCliOptions

task = Terminal_Task()

# python3 example.py -n test -i user/hosts -c user/flexible_network.cfg --authenticate-group cisco_switches  --user orange --password cisco --port 1114

# python3 example.py -n test -i user/hosts -c user/flexible_network.cfg --authenticate-group pa3  --user orange --password cisco --port 1114


# for host in task.devices_dct.values():
#     task.execute(host, "sh version")
# rich.print(task.devices_dct)






task.execute_on_group(group='pa3', cmd="show vlan br")

