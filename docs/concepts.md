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


* This project is designed as Python Library that you import to your Python script that gives you a lot of features and integrations out of the box
* After importing the library you can treat your script as a cli tool that that you use to run tasks, get task logs, list & get backups etc.
[[ Check the [cli parameters](#cli_options) ]]
{: .fs-5 .fw-300 .bg-yellow-000}


> This section gives an overview of how the library works internally

<br>

### 1. Connection Management

This project uses SSH to connect to the devices

**The way it works:** it tries to connect to the selected group of devices, and store the `ssh Channels` of each connected device in a dictionary [ Which you have access to when you create an instance of the class ]

So in simple words, it opens the ssh connection with ALL the selected devices before start executing commands.

And that actually gives us more flexibility from the development perspective, besides *it's much better to be notified if you're NOT able to connect to some devices before starting the automation task* rather than being told at the end of task.

> **NOTE:** any commands you run on the devices *will be exeuted over the same ssh connection*.

![image](https://user-images.githubusercontent.com/33789516/159185347-bbee6112-39e8-4818-93a3-9cea1946fcd1.png)


<br>

### 2. Database

This project uses [TinyDB](https://github.com/msiemens/tinydb) as a local database

This version of Flexible-Network is designed to be used as a Python library / cli tool [ And we didn't want to have any external depedency for it. ] that's why we decided to have a local db per Project directory

* Each project directory has a `.db` directory which stores `database json file`, `tasks logs` and local backups

<br>

### 3. Error Detection

One of the core features in [Flexible-Network](https://github.com/eslam-gomaa/Flexible-Network#features) is the ability to detect error when executing commands on network devices, _So here is how that is done behind the scene:_

* When a command is executed on a network device, fist the library reads the command's output & parse it to see if there is an error
   * And based on that, **if an error is found** we are able to return `stderr` plus we can return `exit_code` of 1 (Which is an indecation of a command that executed with errors)
   * Otherwise, the command is executed successfully & it returns `exit_code` of 0
* Different vendors may have different keywords to search for errors, so we have a [class for each supported vendor](https://github.com/eslam-gomaa/Flexible-Network/tree/develop/FlexibleNetwork/vendors) where the kewords to search are defined as a list eg. `self._stderr_search_keyword`

[check the `execute` method](#execute)


