---
layout: default
nav_order: 1
parent: Python Library
grand_parent: Usage
title: Terminal_Class methods
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


# `Terminal_Task` class Methods
{: .fs-9 }

<br>


```python
from Flexible_Network import Terminal_Task
```


<details markdown="1" id="authenticate">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>authenticate</code></b>
  </summary>
  <br>
   Authenticate with an [inventory](../../inventory.md) group

   > The `authenticate()` method, esablishes SSH conenections with all the hosts of the inventory group (In parallel) 

<br>

INPUT
{: .fs-6 .fw-300 }

| Input                      | Type    | Description                                                  |
| -------------------------- | ------- | ------------------------------------------------------------ |
| `groups`                   | list    | List of group names eg. ['switches', 'test_switches']        |
| `user`                     | string  | Username for authentication                                  |
| `password`                 | string  | Password for authentication                                  |
| `privileged_mode_password` | String  | Password of the Privileged mode  (eg. `enable` in Cisco & `super` in Huawei) [ _If Provided, the device login to `privileged_mode` after authentication._ ] |
| `port`                     | integer | Port for authentication                                      |
|                            |         |                                                              |


<br>

OUTPUT
{: .fs-6 .fw-300 }

> Returns an object with the following attributes

| Input                    | Type    | Description                                                  |
| ------------------------ | ------- | ------------------------------------------------------------ |
| `hosts_total`            | list    | List of the total hosts (of the inventory group/groups) provided for authentication |
| `hosts_connected`        | list    | List the hosts were connected successfully                   |
| `hosts_failed`           | list    | List the hosts failed to connect                             |
| `hosts_total_number`     | integer | Number of total hosts                                        |
| `hosts_connected_number` | integer | Number of connected hosts                                    |
| `hosts_failed_number`    | integer | Number of failed hosts                                       |
| connection_report_table  | string  | Structured table displays connection report of the hosts     |

   ---

</details>


<details markdown="1" id="execute_raw">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>execute_raw()</code></b>
  </summary>

  Execute a command on a remote device.

   <br>

  > **Note:** This method does not print to the terminal.
  
<br>

INPUT
{: .fs-6 .fw-300 }

| Input  | Type   | Description                                                  |
| ------ | ------ | ------------------------------------------------------------ |
| `host` | string | Host to execute commands on ([The host needs to be authenticated first](#authenticate)) |
| `cmd`  | string | The command to execute                                       |


<br>

OUTPUT
{: .fs-6 .fw-300 }

> Returns an objects with the following attributes

| Input     | Type    | Description                                                  |
| --------- | ------- | ------------------------------------------------------------ |
| `host`    | string  | Host to execute commands on (The host needs to be authenticated first) |
| `cmd`     | List    | command (list of lines)                                      |
| stdout    | List    | STDOUT output (list of lines)                                |
| stderr    | List    | STDERR output (list of lines)                                |
| exit_code | Integer | `0` Executed without Errors.     `1` Executed with Errors.     `-1` Connection inturrupted before or during execution |
|           |         |                                                              |



<br>

---

</details>


<details markdown="1" id="execute">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>execute()</code></b>
  </summary>

  Execute a command on a remote device.

   <br>

  > **Note:** This method prints the output to the terminal.
   
   <br>

   INPUT
   {: .fs-6 .fw-300 }


| Input     | Type    | Description                                                  |
| --------- | ------- | ------------------------------------------------------------ |
| `host`    | string  | Host to execute commands on ([The host needs to be authenticated first](#authenticate)) |
| `cmd`     | List    | command (list of lines)                                      |
| stdout    | List    | STDOUT output (list of lines)                                |
| stderr    | List    | STDERR output (list of lines)                                |
| exit_code | Integer | `0` executed without Errors.     `1` Executed with Errors.     `-1` Connection inturrupted before or during execution |
|           |         |                                                              |

   <br>

   OUTPUT
   {: .fs-6 .fw-300 }

   > Returns an object with the following attributes

| Input                   | Type    | Description                                                  |
| ----------------------- | ------- | ------------------------------------------------------------ |
| `host`                  | string  | Host       |
| `cmd`                   | string  | The command to execute                                       |
| only_on_hosts           | List    | **A condition** (List of hosts to execute only on)           |
| skip_hosts              | List    | **A condition** (List of hosts to Skip execution on)         |
| ask_for_confirmation    | Boolean | If **True**,  I will ask for confirmation before executing the command,  *Default: False* |
| exit_on_fail            | Boolean | If **True**, the script will exit if the command exit with an Error,  *Default: True* |
| reconnect_closed_socket | Boolean | If **True**, Try to reconnect to the host if connection was inturrupted (Instead of considering it an error),  *Default: True* |
|                         |         |                                                              |



---

</details>


<details markdown="1" id="execute_from_file">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>execute_from_file()</code></b>
  </summary>

  Load commands from file & execute each line one by one. using the [execute()](#excute) method

   <br>

  > **Note:** This method prints the output to the terminal.
   
   <br>

   INPUT
{: .fs-6 .fw-300 }




| Input                   | Type    | Description                                                  |
| ----------------------- | ------- | ------------------------------------------------------------ |
| `host`                  | string  | Host to execute commands on ([The host needs to be authenticated first](#authenticate)) |
| `file`                  | string  | File with commands to execute                                |
| ask_for_confirmation    | Boolean | If **True**,  I will ask for confirmation before executing the command,  *Default: False* |
| exit_on_fail            | Boolean | If **True**, the script will exit if the command exit with an Error,  *Default: True* |
| reconnect_closed_socket | Boolean | If **True**, Try to reconnect to the host if connection was inturrupted (Instead of considering it an error),  *Default: True* |


   <br>

   OUTPUT
{: .fs-6 .fw-300 }

   > does NOT return

   ---

</details>


<details markdown="1" id="take_config_backup">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>take_config_backup()</code></b>
  </summary>

  Backup running configuration from the remote device & store them in the local directory by default, for other [backup storage options](../../ConfigBackup-storage/backup_config-storage.md)

   <br>

  > **Note:** This method prints the output to the terminal.
   
   <br>

   INPUT
{: .fs-6 .fw-300 }

| Input     | Type   | Description                                   | Options        | Default |
| --------- | ------ | --------------------------------------------- | -------------- | ------- |
| `host`    | string | host to backup its config                     |                |         |
| `comment` | string | A comment indicates the purpose of the backup |                |         |
| `target`  | string | Where to save the backup                      | `local`,  `s3` | `local` |




   > **NOTE:** targets other than `local` requires you to add the credentials in the [config file](../../config_file.md)
   

   <br>

   OUTPUT
{: .fs-6 .fw-300 }

   > Returns an object with the following attributes
   
| Input       | Type    | Description                                                  |
| ----------- | ------- | ------------------------------------------------------------ |
| `exit_code` | Integer | `0` backup taken successfully.      `1` Failed to take backup |
| stderr      | String  | STDERR output                                                |
| stdout      | String  | STDOUT output                                                |
| location    | String  | location, where the backup exists                            |
| id          | String  | The backup string                                            |

---

</details>


<details markdown="1" id="get_config_backup">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>get_config_backup()</code></b>
  </summary>

Return a pre-taken config backup

   <br>

  > **Note:** This method prints the output to the terminal.
   
   <br>

   INPUT
{: .fs-6 .fw-300 }

| Input       | Type   | Description                    | Options | Default |
| ----------- | ------ | ------------------------------ | ------- | ------- |
| `backup id` | string | The ID of the pre-taken backup |         |         |




   > **NOTE:** targets other than 'local' requires you to add the credentials in the config file
   

   <br>

   OUTPUT
{: .fs-6 .fw-300 }

   > Returns an object with the following attributes
   
| Input       | Type    | Description                                                  |
| ----------- | ------- | ------------------------------------------------------------ |
| `exit_code` | Integer | `0` Got backup successfully.      `1` Failed to return backup |
| stderr      | String  | STDERR output                                                |
| stdout      | String  | STDOUT output                                                |
| target      | String  | indicates where the backup is located                        |
| location    | String  | location, where the backup exists                            |
| text        | String  | The backup string                                            |

---

</details>



<br>

---

<br>
