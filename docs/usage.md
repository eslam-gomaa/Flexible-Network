---
layout: default
nav_order: 3
parent: Home
title: Usage
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

# Usage
{: .fs-9 }


There are 2 ways to use Flexible Network:
{: .fs-9 }
- As a Python Library (Use its functions within your Python script)
- Use YAML manifests as Input to Flexible Network (Use almost the same functions provided by the library)






---

1. Create a new directory with a new Python script in it.

> The directory contains your python script is the project directory

```bash
mkdir sample-dir
cd sample-dir
touch my-network-script.py
```

<br>

2. import the `Terminal_Task` class from the `FlexibleNetwork` library & and instantiate an instance of the class

> open your script

```python
from FlexibleNetwork.Flexible_Network import Terminal_Task

# Instantiate an instance of the class 
## that represents a new task in the DB
task = Terminal_Task()

## Start using the available methods ..
```

3. Use the CLI to run the task ( Or list tasks/backups etc... )

```bash
python my-network-script.py -h
```

<br>

* You need the add the hosts you'll automate in an [inentory file](Docs/inventory.md)
* If you plan to use any of the external APIs, make sure you put their information in the [config file](Docs/config_file.md)

<br>

👉 From here, you can take a look at_ the complete [examples](https://eslam-gomaa.github.io/Flexible-Network/examples)
