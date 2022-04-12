---
layout: default
nav_order: 1
parent: Examples
title: 1. Run commands on group of devices
markdown: Kramdown
kramdown:
  parse_block_html: true
  auto_ids: true
  syntax_highlighter: coderay
---


Script used in this example: [example-1.py](docs/Docs/Examples/example-1/example-1.py)

---

```python
from FlexibleNetwork.Flexible_Network import Terminal_Task

# Create an instance of the class
task  = Terminal_Task()


cmd ='''sh vlan br
sh ip int br'''

# Loop over the ONLY authenticated devices
for host in task.connected_devices_dct:
    # Get the "host dictionary" of each device (Contains device information including the SSH channel that will be used for commands execution)
    host_dct = task.connected_devices_dct[host]
    
    # Run enable (enable password is 'cisco')
    enable = task.execute_raw(host_dct, 'enable\n' + 'cisco')
    
    # Run the following commands only if the last command was executed successfully
    if enable['exit_code'] == 0: 
        # Execute a command, the output will be printed to the terminal
        task.execute(host_dct, 'sh ip int br')
        # Execute a command, the output will be printed to the terminal in JSON format
        task.execute(host_dct, cmd, terminal_print='json')
```

In this example we create a script that does the following:
1. Authenticate to the selected inventory group
2. execute set of commands
3. execute commands and the print the output in JSON format

---

### Run the script


##### OUTPUT

```bash
python3.6 docs/Docs/Examples/sample-1.py -n task-1 --config ~/flexible_network.cfg  --inventory user/hots  --authenticate-group works --user orange --password cisco
```

```bash
> Authenticating selected devices
   90.84.41.239  [ 1 / 1 ]          Connected [ 1 ]     Failed [ 0 ]    

> Connection Report   
+--------------+---------------------+-----------+--------------+---------------+-------------------------+---------------+
| Host         | Connection Status   | Comment   |   N of tries |   Max Retries |   Time tring in seconds | Fail Reason   |
+==============+=====================+===========+==============+===============+=========================+===============+
| 90.84.41.239 | 🟢                  | connected |            1 |             3 |                       1 |               |
+--------------+---------------------+-----------+--------------+---------------+-------------------------+---------------+


@ 90.84.41.239
Execution Time: 0.5 seconds
sh ip int br
Interface              IP-Address      OK? Method Status                Protocol
Ethernet0/0            unassigned      YES unset  up                    up      
Ethernet0/1            unassigned      YES unset  up                    up      
Ethernet0/2            unassigned      YES unset  up                    up      
Ethernet0/3            unassigned      YES unset  up                    up      
Ethernet1/0            unassigned      YES unset  up                    up      
Ethernet1/1            unassigned      YES unset  up                    up      
Ethernet1/2            unassigned      YES unset  up                    up      
Ethernet1/3            unassigned      YES unset  up                    up      
Vlan1                  unassigned      YES unset  administratively down down    
Vlan11                 192.168.11.2    YES NVRAM  up                    up      

@ 90.84.41.239
Execution Time: 0.5 seconds
sh vlan br
sh ip int br
{
    "cmd": [
        "sh vlan br",
        "sh ip int br"
    ],
    "exit_code": 0,
    "stderr": [],
    "stdout": [
        "sh vlan br",
        "VLAN Name                             Status    Ports",
        "---- -------------------------------- --------- -------------------------------",
        "1    default                          active    Et1/0, Et1/1, Et1/2, Et1/3",
        "11   mgmt                             active    Et0/0, Et0/2, Et0/3",
        "12   internal                         active    ",
        "13   testing                          active    ",
        "123  testing123 TYPO2                 active    ",
        "1002 fddi-default                     act/unsup ",
        "1003 token-ring-default               act/unsup ",
        "1004 fddinet-default                  act/unsup ",
        "1005 trnet-default                    act/unsup ",
        "sh ip int br",
        "Interface              IP-Address      OK? Method Status                Protocol",
        "Ethernet0/0            unassigned      YES unset  up                    up      ",
        "Ethernet0/1            unassigned      YES unset  up                    up      ",
        "Ethernet0/2            unassigned      YES unset  up                    up      ",
        "Ethernet0/3            unassigned      YES unset  up                    up      ",
        "Ethernet1/0            unassigned      YES unset  up                    up      ",
        "Ethernet1/1            unassigned      YES unset  up                    up      ",
        "Ethernet1/2            unassigned      YES unset  up                    up      ",
        "Ethernet1/3            unassigned      YES unset  up                    up      ",
        "Vlan1                  unassigned      YES unset  administratively down down    ",
        "Vlan11                 192.168.11.2    YES NVRAM  up                    up      "
    ]
}
```

---

##### Screenshoots


![image](https://user-images.githubusercontent.com/33789516/163046526-51cdaab1-445e-41b1-9519-e5bf0018fc8f.png)

![image](https://user-images.githubusercontent.com/33789516/163046595-af67893e-fd80-43f2-82c6-339b4097cad6.png)


