---
layout: default
nav_order: 2
parent: Usage
title: YAML Manifest
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

<link rel="stylesheet" href="{{ site.baseurl }}/css/custom.css">

# Usage _ YAML Manifest Input
{: .fs-9 }


Using Yaml is a simple appreach and does NOT require coding knowledge, the steps are simple:
{: .fs-6 .fw-300 }

- Import `Flexible-Network` library in your Python script
- Write your Yaml manifest
- Run your script !


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

<script src="https://gist.github.com/eslam-gomaa/0294b7c1a8d624341e7842732e1941e3.js"></script>


```bash
vi test.yaml
```

<script src="https://gist.github.com/eslam-gomaa/10b729e7ce499f2cbebd4c688529b812.js"></script>


```bash
python3 my_script.py --file test.yaml
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
