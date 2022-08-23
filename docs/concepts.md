---
layout: default
nav_order: 1
parent: Home
title: Concepts
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

# How it works !
{: .fs-9 }


- This project provides you with a **Python Library** that you import to your Python script which gives you a lot of features and integrations out of the box
- After importing the library you can treat your script as a cli tool that you use to run network automation tasks
- The library gives you a lot of useful functions for network automation, besides saving each automation task & backups in a local DB, and with CLi options you retrieve task logs or config backups
- The library gives you out of the box [integration](./Docs/Integrations/integrations.md) with external APIs, for example saving config backups on remote locations like [object storage](./Docs/ConfigBackup-storage/s3.md) (eg. any compatable s3 object storage) or getting credentials from a secret manager like Vault or Cyberark


> This section gives an overview of how the library works internally

<br>

### 1. Connection Management

This project uses SSH to connect to the network devices

**The way it works:** it connects with the choosen [intentory](./Docs/inventory.md) group, and stores the `ssh Channel` of each connected device in memory.

So in simple words, it opens the ssh connection with ALL the selected devices before start executing commands.
That acutally provides a way to get a connection report and get notified if any device is down before start executing commands

> **NOTE:** If the connection was interrupted before the exection for any reason, the library will to try to reconnect instead raising and error.

![image](https://user-images.githubusercontent.com/33789516/159185347-bbee6112-39e8-4818-93a3-9cea1946fcd1.png)


<br>

### 2. Database

This project uses [TinyDB](https://github.com/msiemens/tinydb) as a local database

This version of Flexible-Network is designed to be used as a **Python library / cli tool** [ And we didn't want to have any external depedency for it. ] that's why we decided to have a local db per Project directory

* Each project directory has a `.db` directory which stores `database json file`, `tasks logs` and `local backups`

<br>

### 3. Error Detection

One of the core features in [Flexible-Network](https://github.com/eslam-gomaa/Flexible-Network#features) is the ability to detect errors when executing commands on network devices, _So here is how that is done behind the scene:_

* When a command is executed on a network device, fist the library reads the command's output & parse it to see if there is an error
  - And based of that information, we're able to return `exit_code`, `stderr`, and `stdout`

* Different vendors may have different keywords to search for errors, so we have a [class for each supported vendor](https://github.com/eslam-gomaa/Flexible-Network/tree/develop/FlexibleNetwork/vendors) where the kewords to search are defined as a list eg. `self._stderr_search_keyword`

[check [`execute()` method](./Docs/usage/library_usage/class_methods.md#execute)


