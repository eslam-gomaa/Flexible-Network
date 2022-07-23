import rich
from numpy import rint
from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Flexible_Network import ReadCliOptions 

task = Terminal_Task()

# python3 example.py -n test -i user/hosts -c user/flexible_network.cfg --authenticate-group cisco_switches  --user orange --password cisco --port 1114

# python3 example.py -n test -i user/hosts -c user/flexible_network.cfg --authenticate-group pa3  --user orange --password cisco --port 1114


# for host in task.devices_dct.values():

#     task.execute(host, "sh version")

# 
# rich.print(task.devices_dct)

def execute_test(devices_dct, cmd, parallel=False, parallel_threads=5):
    if not parallel:
        for host in devices_dct.values():
            if host['is_connected']:
                task.execute(host_dct=host, cmd=cmd)
            else:
                if ReadCliOptions.debug:
                    rich.print(f"\nDEBUG -- [bold]HOST:[/bold] {host['host']} skipped, [bold]REASON[/bold]: [bright_red]{host['fail_reason']}[/bright_red]")
                    rich.print(host)



execute_test(task.devices_dct, "show vlan br")

