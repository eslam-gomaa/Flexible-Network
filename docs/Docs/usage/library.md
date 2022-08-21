---
layout: default
nav_order: 1
parent: Usage
title: Python Library
markdown: Kramdown
kramdown:
  parse_block_html: true
  auto_ids: true
  syntax_highlighter: coderay
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

# Usage | Library
{: .fs-9 }


Getting started with the Flexible-Network Library is simple:
{: .fs-9 }

- Import it within your Python script
- Make sure that you've added the hosts in the inventory file
- Use `.authenticate()` method to connect to the choosen group of devices
  - It returns an object with few attributes, we need to use `hosts_connected` attribute (as it contains the devices that were connected successfully (List) )
- Loop through `hosts_connected` list and use methods you need
- Use cli to run your script


### Getting started Example
{: .fs-9 }


```
vi /etc/flexible_network/hosts
```
```ini
[switches]
192.168.1.12
192.168.1.13
192.168.1.11
```

```bash
vi my_script.py
```

```python
from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Vendors import Cisco

# This will initialize the class .. Create a DB record, use cli, read config, etc.
task = Terminal_Task()

# That's the default vendor
task.vendor = Cisco()

auth = task.authenticate(groups='switches',
                         user='my_user',
                         password='my_password',
                         privileged_mode_password='my_password',
                         port=22)


for host in auth.hosts_connected:
  # Take a config backup, target local will save the backup on the disk
    task.take_config_backup(host, "Test", target='local')
    task.execute(host, "sho ip int br")
    task.execute(host, "sho vlan br") 
```

```bash
python3 my_script.py --name "Test task"
```


List the tasks, you'll find your task at the end

```bash
python3 my_script.py --task --list

python3 my_script.py --task --get-log <TASK-ID>
```


If've taken backups, you can list them as well

```bash
python3 my_script.py --backup --list

python3 my_script.py  --backup --get-backup <BACKUP-ID>
```