---
layout: default
nav_order: 2
permalink: /
title: Inventory
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

# Inventory

We use the same inventory concept as Ansible, Here is an example of an inventory file

> This inventory has 4 groups `testing`, `switches`, `routers` and `empty`, each contains the devices listed below it

```ini
[testing]
192.168.100.4

[switches]
192.168.1.10
192.168.1.11

[routers]
192.168.1.12
192.168.1.13
192.168.1.11

[empty]
```

<br>

> **Note:** _Custom inventory parameters_ will be considered in the next milestone.


<br>

---

<br>


### Inventory location

the default inventory location can be specified in the [configuration file](config_file.md#sample_config_file)

```ini
[general]
default_inventory = /etc/flexible-network/hosts
```


<br>

Alternatively you can provide a custom inventory file with the `--inventory` or `-i` CLI option




