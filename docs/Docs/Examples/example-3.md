---
layout: default
nav_order: 3
parent: Examples
title: 3. Execute commands from a file && send a connection report to RocketChat
markdown: Kramdown
kramdown:
  parse_block_html: true
  auto_ids: true
  syntax_highlighter: rouge
---

<button class="btn js-toggle-dark-mode">Switch to Dark Mode

<script>
const toggleDarkMode = document.querySelector('.js-toggle-dark-mode');

jtd.addEvent(toggleDarkMode, 'click', function(){
  if (jtd.getTheme() === 'dark') {
    jtd.setTheme('light');
    toggleDarkMode.textContent = 'Switch to Dark Mode';
  } else {
    jtd.setTheme('dark');
    toggleDarkMode.textContent = 'Switch to Light Mode';
  }
});
</script>


Script used in this example can be found in this directory: [Examples](https://github.com/eslam-gomaa/Flexible-Network/tree/develop/docs/Docs/Examples)

In this example we create a script that does the following:
1. Authenticate to the selected [inventory](https://eslam-gomaa.github.io/Flexible-Network/inventory) group (Using CLI)
2. [execute commands from file](https://eslam-gomaa.github.io/Flexible-Network/terminal_class_methods#execute_from_file)
3. Generate a connection report & send it via [RocketChat](https://eslam-gomaa.github.io/Flexible-Network/Docs/Integrations/rocketchat/)


---

<script src="https://gist.github.com/eslam-gomaa/889ee9ec1e4789afce718339d9493f5b.js"></script>

---

### Run the script

```bash
python3.6 docs/Docs/Examples/sample-3.py -n task-3 --config ~/flexible_network.cfg  --inventory user/hots  --authenticate-group works --user orange --password cisco
```

### OUTPUT


```bash
> Authenticating selected devices
   90.84.41.239  [ 1 / 1 ]          Connected [ 1 ]     Failed [ 0 ]    

> Connection Report   
+--------------+---------------------+-----------+--------------+---------------+-------------------------+---------------+
| Host         | Connection Status   | Comment   |   N of tries |   Max Retries |   Time tring in seconds | Fail Reason   |
+==============+=====================+===========+==============+===============+=========================+===============+
| 90.84.41.239 | 🟢                  | connected |            1 |             3 |                       1 |               |
+--------------+---------------------+-----------+--------------+---------------+-------------------------+---------------+


WARNING -- Confirm before running the following command: 

sh ip int br 
show vlan br
show version

yes || no 

yes: Run & continue
no:  Abort
YOUR Decision: yes
> Ok .. Let's continue ...


@ 90.84.41.239
Execution Time: 0.5 seconds
sh ip int br 
{
    "cmd": [
        "sh ip int br "
    ],
    "exit_code": 0,
    "stderr": [],
    "stdout": [
        " ",
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


@ 90.84.41.239
Execution Time: 0.5 seconds
show vlan br
{
    "cmd": [
        "show vlan br"
    ],
    "exit_code": 0,
    "stderr": [],
    "stdout": [
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
        "1005 trnet-default                    act/unsup "
    ]
}


@ 90.84.41.239
Execution Time: 0.5 seconds
show version
{
    "cmd": [
        "show version"
    ],
    "exit_code": 0,
    "stderr": [],
    "stdout": [
        "Cisco IOS Software, Linux Software (I86BI_LINUXL2-ADVENTERPRISEK9-M), Version 15.2(CML_NIGHTLY_20150703)FLO_DSGS7, EARLY DEPLOYMENT DEVELOPMENT BUILD, synced to  DSGS_PI5_POSTCOLLAPSE_TEAM_TRACK_CLONE",
        "Technical Support: http://www.cisco.com/techsupport",
        "Copyright (c) 1986-2015 by Cisco Systems, Inc.",
        "Compiled Sat 04-Jul-15 01:30 by mmen",
        "ROM: Bootstrap program is Linux",
        "mgmt_sw uptime is 1 week, 1 day, 10 hours, 43 minutes",
        "System returned to ROM by reload at 0",
        "System image file is \"unix:/opt/unetlab/addons/iol/bin/L2-ADVENTERPRISEK9-M-15.2-20150703.b\"",
        "Last reload reason: Unknown reason",
        "This product contains cryptographic features and is subject to United",
        "States and local country laws governing import, export, transfer and",
        "use. Delivery of Cisco cryptographic products does not imply",
        "third-party authority to import, export, distribute or use encryption.",
        "Importers, exporters, distributors and users are responsible for",
        "compliance with U.S. and local country laws. By using this product you",
        " --More-- \b\b\b\b\b\b\b\b\b        \b\b\b\b\b\b\b\b\b"
    ]
}
```

