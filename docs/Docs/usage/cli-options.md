---
layout: default
nav_order: 3
parent: Usage
title: Cli Options
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

# CLI Options
{: .fs-9 }


<br>

#### General
{: .fs-6 .fw-300 }

<details markdown="1" id="--inventory">
  <summary markdown="span"> 
  <b style="font-size:20px"> <code>--inventory</code></b>
  </summary>
   A file that contains the devices to automate

   Optional
   {: .label .label-green }
   
   > This argument overrides the following option in the config file.
   >```ini
   >[general]
   >default_inventory = /etc/flexible-network/hosts
   >```

   ---

</details>


<details markdown="1" id="--no-confirm-auth">
  <summary markdown="span"> 
  <b style="font-size:20px"> <code>--no-confirm-auth</code></b>
  </summary>
  Skip Asking for confirmation if failed to connect to some deivces
  
  Optional
  {: .label .label-green }

  > The dfault Behavior is to ask you for confirmation before proceeding if failed to authenticate to some devices.
</details>


<details markdown="1" id="--config">
  <summary markdown='span'>
  <b style="font-size:20px"> <code>--config</code></b>
  </summary>
  Specify a custom configuration file path (Overrides the default configuration file path)
  
  Optional
  {: .label .label-green }

  > Default configuration file path is `/etc/flexible_network/flexible_network.cfg`

---

</details>

<br>

#### Run a task  [ [Python Script](./library_usage/library.md) ]
{: .fs-6 .fw-300 }

<details markdown="1" id="--name">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>--name</code></b>
  </summary>
   The task name

   Optional
   {: .label .label-yellow }
   
   > Each script run represents a task, Tasks state are stored in the local directory (small local DB)

   ---

</details>


<br>

#### Run a task  [ [Yaml file](./yaml_usage/yaml_manifest.md) ]
{: .fs-6 .fw-300 }


<details markdown="1" id="--file">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>--file</code></b>
  </summary>
  Pass a yaml file as input
  
  Optional
  {: .label .label-yellow }

  ---

</details>

<br>

#### get tasks
{: .fs-6 .fw-300 }


<details markdown="1" id="--task">
  <summary markdown='span'>
  <b style="font-size:20px"> <code>--task</code></b>
  </summary>
  Perform operations on finished tasks
  
  required
  {: .label .label-yellow }

---

</details>

<details markdown="1" id="--list">
  <summary markdown='span'>
  <b style="font-size:20px"> <code>--list</code></b>
  </summary>
  List the finished tasks
  
  Optional
  {: .label .label-green }

---

</details>


<details markdown="1" id="--get-log">
  <summary markdown='span'>
  <b style="font-size:20px"> <code>--get-log</code></b>
  </summary>
  Return the log of the task

  Takes the `task ID`
  
  Optional
{: .label .label-green }

---

</details>



<br>

#### get backups
{: .fs-6 .fw-300 }

<details markdown="1" id="--backup">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>--backup</code></b>
  </summary>
  Perform operations on taken configuration backups
  
  required
  {: .label .label-yellow }

  ---

</details>


<details markdown="1" id="--list-backup">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>--list</code></b>
  </summary>
  List the taken configuration backups

  Optional
  {: .label .label-green }

---

</details>


<details markdown="1" id="--get-backup">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>--get-backup</code></b>
  </summary>
  Return the configuration backup for the selected device

  Takes the `backup ID`
  
  Optional
  {: .label .label-green }

---

</details>

<br>

<details markdown="1" id="--all">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>--all</code></b>
  </summary>
  When listing tasks or backups, it lists the last 15 item by default, to list all use `--all` or `-A` option
  
  Optional
  {: .label .label-green }

---

</details>

<br>

#### Validate the integration with the external APIs
{: .fs-6 .fw-300 }

<details markdown="1" id="--validate-integration">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>--validate-integration</code></b>
  </summary>
   Validate the communication with any of the supported API Integrations eg. test to authenticate (And validate permissions if needed).

  Optional
  {: .label .label-green }

  * ***Supported Options***
      * `cyberArk`
      * `rocketChat`
      * `s3`

  ---

</details>

<br>

_**Example**_

```bash
python3.6 <script.py> -c ~/flexible_network.cfg  --validate-integration s3 rocketChat

> Validating Integration
+---------------+----------+-----------+
| Integration   | Status   | Comment   |
+===============+==========+===========+
| rocketChat    | 🟢       | Works !   |
+---------------+----------+-----------+
| S3            | 🟢       | Works !   |
+---------------+----------+-----------+
```


<br>

<br>

## Deprecated (To be refactored in the next release)


<details markdown="1" id="--authenticate-group">
  <summary markdown="span"> 
  <b style="font-size:20px"> <code>--authenticate-group</code></b>
  </summary>
   Provide an inventory group to authenticate
   
   Optional
   {: .label .label-green }



> **Note:** this option requires to specify the [`--user`](#--user) & [`--password`](#--password)  arguments 

> Example
```java
python3.6 test1.py -n task1 \
   --config user/flexible_network.cfg \
   --inventory user/hosts \
   --authenticate-group works \
   --user orange --password cisco1 --port 1113
```


<br>

<br>

-> This will update the `devices_dct` & `connected_devices_dct` attributes in the `Terminal_Task` class (Which you can access after you instantiate an instance of the class)

```python
task = Terminal_Task()

# A dict that contains ONLY the connected devices
task.connected_devices_dct

# A dict that contails ALL the devices (including ones that failed to authenticate)
task.devices_dct
```

---

</details>


<details markdown="1" id="--user">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>--user</code></b>
  </summary>
  The user to authenticate the group with

  Optional
  {: .label .label-green }

  ---

</details>


<details markdown="1" id="--password">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>--password</code></b>
  </summary>
  The password to authenticate the group with

  Optional
  {: .label .label-green }

  ---

</details>


<details markdown="1" id="--port">
  <summary markdown='span'>
  <b style="font-size:20px"> <code>--port</code></b>
  </summary>
  The port to use to connect to the group.

  Optional
  {: .label .label-green }

  > default port is `22`

  ---

</details>