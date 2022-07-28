from FlexibleNetwork.Flexible_Network import Terminal_Task
task = Terminal_Task()

# python3 example.py -n test -i user/hosts -c user/flexible_network.cfg --authenticate-group cisco_switches  --user orange --password cisco --port 1114

# python3 example.py -n test -i user/hosts -c user/flexible_network.cfg --authenticate-group pa3  --user orange --password cisco --port 1114


# for host in task.devices_dct.values():
#     task.execute(host, "sh version")
# rich.print(task.devices_dct)


# For each host in the group execute the listed commands
# task.execute_on_group(group='pa3', cmd=[
#                                         "show vlan br",
#                                         "show ip int br"
#                                         ])



task.sub_task(group='works', cmds=[
    {
        "command": "show ip int br", 
        "tag": "123df",
    },
    {
        "command": "show vlan br", 
        "when": {"tag": "123df", "exit_code": 1, 'operator': 'is'}
    },
    {
        "command": "show vlan br", 
    }
])


