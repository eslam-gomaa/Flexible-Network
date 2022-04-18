---
layout: default
nav_order: 1
parent: Examples
title: 1. Run commands on group of devices
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
2. [execute ](https://eslam-gomaa.github.io/Flexible-Network/terminal_class_methods#execute) set of commands
3. execute commands and the print the output in JSON format


---

<link href="_sass/support/_variables.scss" rel="stylesheet" type="text/css">


<script src="https://gist.github.com/eslam-gomaa/c29f3b6c04430bc676231044252fa961.js"></script>

---

### Run the script

```bash
python3.6 docs/Docs/Examples/sample-1.py -n task-1 --config ~/flexible_network.cfg  --inventory user/hots  --authenticate-group works --user orange --password cisco
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

#### Screenshoots


![image](https://user-images.githubusercontent.com/33789516/163046526-51cdaab1-445e-41b1-9519-e5bf0018fc8f.png)

![image](https://user-images.githubusercontent.com/33789516/163046595-af67893e-fd80-43f2-82c6-339b4097cad6.png)


