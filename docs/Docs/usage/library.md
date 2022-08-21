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


# Usage _ Python Library
{: .fs-9 }


Getting started with the Flexible-Network Library is simple:
{: .fs-6 .fw-300 }

- Import `Flexible-Network` library in your Python script
- Make sure that you've added the hosts in the inventory file
- Use `.authenticate()` method to connect to the choosen group of devices
  - It returns an object with few attributes, we need to use `hosts_connected` **(List)** attribute (as it contains the devices that were connected successfully)
- Loop through `hosts_connected` list and use the methods you need
- Use cli options to run your script


### Getting started Example
{: .fs-6 .fw-300 }


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

<link rel="stylesheet" href="{{ site.baseurl }}/css/custom.css">


<script src="https://gist.github.com/eslam-gomaa/e965313db0ddbfcc21f095bea6603e91.js"></script>


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
