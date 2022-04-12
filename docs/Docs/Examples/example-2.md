---
layout: default
nav_order: 2
parent: Examples
title: 2. Take config backup
markdown: Kramdown
kramdown:
  parse_block_html: true
  auto_ids: true
  syntax_highlighter: coderay
---


Script used in this example: [example-2.py](example-2.py)

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
        # Backup config and store the backup to S3 (In this example "Openstack object storage")
        task.backup_config(host_dct, 'Testing S3 integrations', target='s3')
```

In this example we create a script that does the following:
1. Authenticate to the selected inventory group
2. execute set of commands
3. execute commands and the print the output in JSON format

---

### Run the script


##### OUTPUT

```bash
python3.6 docs/Docs/Examples/sample-2.py -n task-1 --config ~/flexible_network.cfg  --inventory user/hots  --authenticate-group works --user orange --password cisco
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
backup-config-eslam-5

@ 90.84.41.239
> backup taken successfully > [ Testing S3 integrations ]
```

---

##### Screenshoots


![image](https://user-images.githubusercontent.com/33789516/163047768-910992cd-035d-4996-8198-d11c294ccdca.png)


---

#### List the backups

```bash
python3.6 docs/Docs/Examples/sample-2.py --backup --list
```

```
| a893500c-836e-4d22-94b9-e4980be1fe00 | Testing S3 integrations  | 90.84.41.239 | s3       | 🟢 success | 29-03-2022 | 10-47-05 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
| 4d6fae23-8c80-417a-bafb-af617b6dd5ba | test                     | 90.84.41.239 | local    | 🔴 failed  | 01-04-2022 | 06-10-32 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
| 41ce52a6-0c03-4efe-a29d-07ef752c53f0 | test                     | 90.84.41.239 | local    | 🟢 success | 01-04-2022 | 06-13-12 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
| e02e2910-c3b3-4e25-9f1c-19fa389f1710 | test                     | 90.84.41.239 | local    | 🟢 success | 01-04-2022 | 06-14-09 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
| 116ba93e-4e90-4e33-9b39-0b89b37e648e | test                     | 90.84.41.239 | local    | 🟢 success | 01-04-2022 | 06-14-32 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
| 53a63787-6f26-4d23-89c5-18a71471bc50 | Testing S3 integrations  | 90.84.41.239 | s3       | 🟢 success | 12-04-2022 | 20-25-50 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
```

![image](https://user-images.githubusercontent.com/33789516/163048128-21054160-d338-4475-8711-766942cdf62d.png)
