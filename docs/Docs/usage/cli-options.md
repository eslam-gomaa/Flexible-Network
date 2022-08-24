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

</details>

<br>

<details markdown="1" id="--delete">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>--delete</code></b>
  </summary>
  Delete a task or backup

  **Example**
  
```bash
python3 example2.py --task --list

+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| id                                   | name        | log format   |   n_of_backups |   n_of_hosts |   n_of_connected_hosts | date       | time     |
+======================================+=============+==============+================+==============+========================+============+==========+
| 5205f5d5-579d-4abd-8097-5a19103d25ec | New Task    | markdown     |              0 |            0 |                      0 | 21-08-2022 | 10:06:55 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| c2ca1dc3-3b24-40f0-a1e8-71cb283bb844 |             | markdown     |              0 |            0 |                      0 | 21-08-2022 | 10:07:03 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| 792c2635-bb4f-4eef-9c3a-b031226eef6c | New Task    | markdown     |              0 |            1 |                      1 | 21-08-2022 | 10:07:07 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| 9252bc8c-1258-479b-9953-8a590cd9ebf8 | new-day     | markdown     |              2 |            1 |                      1 | 21-08-2022 | 10:07:40 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| 76d458f1-1cf8-4275-90b4-6d31c61e8b37 | New Task    | markdown     |              0 |            0 |                      0 | 21-08-2022 | 22:27:42 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| a56e9835-d777-4360-b673-ef66d7d2d1af | New Task    | markdown     |              0 |            0 |                      0 | 21-08-2022 | 22:27:54 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| 7c6c061a-f183-43e3-a3ba-d219d2977044 | New Task    | markdown     |              0 |            1 |                      0 | 21-08-2022 | 22:28:07 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| 65fe4a22-f2aa-4815-b675-2d18ef35473f | New Task    | markdown     |              0 |            1 |                      1 | 21-08-2022 | 22:28:18 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| a6535ba0-3a62-4054-8c05-af8704845057 | New Task    | markdown     |              0 |            1 |                      1 | 21-08-2022 | 22:31:02 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| b0825f73-7a13-42b6-911d-aeb9350c0e6d | New Task    | markdown     |              0 |            1 |                      0 | 21-08-2022 | 22:35:20 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| 99e40d7b-3e99-4de0-8093-b3c2d0b083ea | New Task    | markdown     |              0 |            1 |                      1 | 21-08-2022 | 22:35:28 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| 83269073-9753-4029-8712-773f6196fd04 | New Task    | markdown     |              1 |            1 |                      1 | 21-08-2022 | 22:37:48 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| 063c81c6-fe7d-4cbf-a14e-c061b5de8f18 | Test task   | txt          |              0 |            1 |                      0 | 22-08-2022 | 22:52:16 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| 37c06183-c5a9-44d3-b4bd-34138b5c1e89 | Test task 2 | txt          |              0 |            1 |                      0 | 22-08-2022 | 22:56:45 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+
| 26678911-2ef6-4ba9-bbfa-caabcb929bb8 | Test task   | txt          |              2 |            1 |                      1 | 24-08-2022 | 08:11:22 |
+--------------------------------------+-------------+--------------+----------------+--------------+------------------------+------------+----------+

python3 example2.py --task --delete 26678911-2ef6-4ba9-bbfa-caabcb929bb8
# INFO -- task with name 'Test task' deleted successfully
```

```bash
python3 example2.py --backup --list

+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| id                                   | comment     | host         | target   | status     | date       | time     |
+======================================+=============+==============+==========+============+============+==========+
| 92c5d552-5366-45fc-8051-1820b0907a6a | test backup | 90.84.41.239 | local    | 🟢 success | 19-08-2022 | 19:10:14 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| 7a1fd365-a9d4-4d3e-bc2f-774008bbbe33 | Test backup | 90.84.41.239 | local    | 🟢 success | 19-08-2022 | 19:53:25 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| 6768c9c4-6fb8-4a62-bd2d-a987d62f7958 | Test backup | 90.84.41.239 | local    | 🔴 failed  | 19-08-2022 | 19:57:22 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| 78248920-6945-49d5-a2b8-b1be18c49b48 | Test backup | 90.84.41.239 | local    | 🟢 success | 19-08-2022 | 19:59:32 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| ed0820b8-d995-4fda-8306-3abe88857461 | Test backup | 90.84.41.239 | local    | 🟢 success | 19-08-2022 | 20:05:33 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| 7a3b64a8-90c8-4246-85eb-d852fd3a2685 | Test        | 90.84.41.239 | local    | 🟢 success | 20-08-2022 | 18:13:50 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| e44405ce-ced3-4637-b0ae-916bd12ab7cc | test backup | 90.84.41.239 | local    | 🟢 success | 20-08-2022 | 18:13:52 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| 783219c2-e4f7-4e25-8c48-fdea80a5ae51 | Test        | 90.84.41.239 | local    | 🟢 success | 20-08-2022 | 18:34:06 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| aa7f8bc4-5c86-4341-b962-b1270fa3ca0b | test backup | 90.84.41.239 | local    | 🟢 success | 20-08-2022 | 18:34:08 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| 393c36ae-3d3c-4093-b62b-0aac29a502a9 | Test backup | 90.84.41.239 | local    | 🟢 success | 20-08-2022 | 18:37:40 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| 1354d07f-ac1e-4028-85a0-5797f092d3ca | Test        | 90.84.41.239 | local    | 🟢 success | 21-08-2022 | 10:07:45 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| d6a3295f-d966-4f56-a462-c495e2c5378b | test backup | 90.84.41.239 | local    | 🟢 success | 21-08-2022 | 10:07:48 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| 0fea8f3d-3521-4091-974f-e4ad02ad26f9 | Test backup | 90.84.41.239 | local    | 🟢 success | 21-08-2022 | 22:38:00 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| 305678fe-a79f-4e6b-96c1-b1f01436a339 | Test        | 90.84.41.239 | local    | 🟢 success | 24-08-2022 | 08:11:28 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+
| 34437355-ebb5-4dd5-9eae-b08006a11379 | test backup | 90.84.41.239 | local    | 🟢 success | 24-08-2022 | 08:11:30 |
+--------------------------------------+-------------+--------------+----------+------------+------------+----------+

python3 example2.py --backup --delete 305678fe-a79f-4e6b-96c1-b1f01436a339
# INFO -- backup with comment 'Test' deleted successfully, Host: 90.84.41.239 , Target: local
```

  
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