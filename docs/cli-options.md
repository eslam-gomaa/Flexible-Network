---
layout: default
nav_order: 99
parent: Home
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


### Run a task

<details markdown="1" id="--name">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>--name</code></b>
  </summary>
   The task name

   Required
   {: .label .label-yellow }
   
   > Each script run represents a task, Tasks state are stored.

   ---

</details>


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

<details markdown="1" id="--authenticate-group">
  <summary markdown="span"> 
  <b style="font-size:20px"> <code>--authenticate-group</code></b>
  </summary>
  <br>
   Privide an inventory group to authenticate
   
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

-> This will update the `devices_dct` & `connected_devices_dct` attributes in the `Terminal_Task` class (Which you can access after you instanciate an instance of the class)

```python
task = Terminal_Task()

# A dict that contains ONLY the connected devices
task.connected_devices_dct

# A dict that contails ALL the devices (including ones that failed to authenticate)
task.devices_dct
```

---

</details>


<details markdown="1" id="--no-confirm-auth">
  <summary markdown="span"> 
  <b style="font-size:20px"> <code>--no-confirm-auth</code></b>
  </summary>
  <br>
  Skip Asking for confirmation if failed to connect to some deivces
  
  > *Optional*

  > The dfault Behavior is to ask you for confirmation before proceeding if failed to authenticate to some devices.
</details>

<br>

<a id=--user></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--user</code></b>
  </summary>
  <br>
  The user to authenticate the group with

  > *Optional*

  ---

</details>


<a id=--password></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--password</code></b>
  </summary>
  <br>
  The password to authenticate the group with

  > *Optional*

  ---

</details>


<a id=--port></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--port</code></b>
  </summary>
  <br>
  The port to use to connect to the group.

  > *Optional*

  > default port is `22`
</details>

<a id=--config></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--config</code></b>
  </summary>
  <br>
  Specify a custom configuration file path (Overrides the default configuration file path)
  
  > *Optional*

  > Default configuration file path is `/etc/flexible_network/flexible_network.cfg`
</details>


<br>

### get tasks

<a id=--task></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--task</code></b>
  </summary>
  <br>
  Perform operations on finished tasks
  
  > *Optional*

</details>

<a id=--list></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--list</code></b>
  </summary>
  <br>
  List the finished tasks
  
  > *Optional*

</details>


<a id=--get-log></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--get-log</code></b>
  </summary>
  <br>
  Return the log of the task

  Takes the `task ID`
  
  > *Optional*

</details>


<br>

### get backups


<a id=--backup></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--backup</code></b>
  </summary>
  <br>
  Perform operations on taken configuration backups
  
  > *Optional*

</details>

<a id=--list-backup></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--list</code></b>
  </summary>
  <br>
  List the taken configuration backups
  
  > *Optional*

</details>

<a id=--get-backup></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--get-backup</code></b>
  </summary>
  <br>
  Return the configuration backup for the selected device

  Takes the `backup ID`
  
  > *Optional*

</details>


<br>

### Validate the integration with the external APIs


<a id=--validate-integration></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--validate-integration</code></b>
  </summary>
  <br>
   Validate the communication with any of the supported API Integrations eg. test to authenticate (And validate permissions if needed).
  <br>

  > *Optional*

  * ***Supported Options***'
      * `cyberArk`
      * `rocketChat`
      * `s3`

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

