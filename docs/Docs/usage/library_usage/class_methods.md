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
|                          |         |                                                              |


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
| `host`    | string  | Host to execute commands on (The host needs to be authenticated first) |
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
| `host`                  | string  | Host to execute commands on ([The host needs to be authenticated first](#authenticate)) |
| `cmd`                   | string  | The command to execute                                       |
| only_on_hosts           | List    | **A condition** (List of hosts to execute only on)           |
| skip_hosts              | List    | **A condition** (List of hosts to Skip execution on)         |
| ask_for_confirmation    | Boolean | If **True**,  I will ask for confirmation before executing the command,  *Default: False* |
| exit_on_fail            | Boolean | If **True**, the script will exit if the command exit with an Error,  *Default: True* |
| reconnect_closed_socket | Boolean | If **True**, Try to reconnect to the host if connection was inturrupted (Instead of considering it an error),  *Default: True* |
|                         |         |                                                              |



### Sample Output

[The same as `execute_raw` method](#execute_raw)

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


   | Input                  | Type  | Description                                                  | Options            | Default   |
   | ---------------------- | ----- | ------------------------------------------------------------ | ------------------ | --------- |
   | `hos_dct`              | dct   | The host dictionary => is key of the  `connected_devices_dct` attribute  (And contains information about the device including the `ssh channel` to use for the command execution ) |                    |           |
   | `file`                 | str   | The file to load the commands from                      |                    |           |
   | `terminal_print`       | str   | Print the ouput \|\| error to the terminal                   | 'default',  'json' | 'default' |
   | `ask_for_confirmation` | bool  | Ask for confirmation before executing a command,             |                    | False     |
   | `exit_on_fail`         | boola | Exit the script with code of `1` if the command executed with errors |                    | True      |


   <br>

   OUTPUT
{: .fs-6 .fw-300 }

   > does NOT return

   ---

</details>


<details markdown="1" id="connection_report_Table">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>connection_report_Table()</code></b>
  </summary>
   Return a structured table describes the authentication status of the selected devices

* Input
   1. Is the `devices_dct` attribute (Which is a dictionary that is populated when you called the `authenticate()` methd and contains the authentication info of each device) 

> **Note:** the method does NOT print the output to the terminal by default, but you're able to print the variable as the following example.

```python
report = task.connection_report_Table(task.devices_dct)
print(report)
```

> You can also send it as a message
> * Check out the RocketChat Integration

```python
rocket_msg = rocket.send_message(['eslam.gomaa'], "``` {} ```".format(report))
# print(rocket_msg)
```

<br>
<br>



**Sample Output**

```
+----------------+---------------------+-----------------+--------------+---------------+-------------------------+------------------------+
| Host           | Connection Status   | Comment         |   N of tries |   Max Retries |   Time tring in seconds | Fail Reason            |
+================+=====================+=================+==============+===============+=========================+========================+
| 90.84.41.239   | 🟢                  | connected       |            1 |             3 |                       1 |                        |
+----------------+---------------------+-----------------+--------------+---------------+-------------------------+------------------------+
| 90.84.41.2     | 🔴                  | Fail to connect |            3 |             3 |                      16 | NOT able to establish  |
|                |                     |                 |              |               |                         | an ssh connection with |
|                |                     |                 |              |               |                         | 90.84.41.2 on port     |
|                |                     |                 |              |               |                         | 1113 >> timed out      |
+----------------+---------------------+-----------------+--------------+---------------+-------------------------+------------------------+
| 192.168.1.241  | 🔴                  | Fail to connect |            3 |             3 |                      16 | NOT able to establish  |
|                |                     |                 |              |               |                         | an ssh connection with |
|                |                     |                 |              |               |                         | 192.168.1.241 on port  |
|                |                     |                 |              |               |                         | 1113 >> timed out      |
+----------------+---------------------+-----------------+--------------+---------------+-------------------------+------------------------+
| 192.168.1.2452 | 🔴                  | Fail to connect |            1 |             3 |                       0 | Could NOT resolve      |
|                |                     |                 |              |               |                         | hostname               |
|                |                     |                 |              |               |                         | 192.168.1.2452 Name or |
|                |                     |                 |              |               |                         | service not known >>   |
|                |                     |                 |              |               |                         | [Errno -2] Name or     |
|                |                     |                 |              |               |                         | service not known      |
+----------------+---------------------+-----------------+--------------+---------------+-------------------------+------------------------+
```

---

</details>


<details markdown="1" id="backup_config">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>backup_config()</code></b>
  </summary>

  Backup running configuration from the remote device & store them in the local directory by default, for other backup storage options check [supported backup targets]

   <br>

  > **Note:** This method prints the output to the terminal.
   
   <br>

   INPUT
{: .fs-6 .fw-300 }

   | Input     | Type | Description                                                  | Options        | Default |
   | --------- | ---- | ------------------------------------------------------------ | -------------- | ------- |
   | `hos_dct` | dct  | The host dictionary => is key of the  `connected_devices_dct` attribute  (And contains information about the device including the `ssh channel` to use for the command execution ) |                |         |
   | `comment` | str  | A comment indicates the purpose of the backup                |                |         |
   | `target`  | str  | Print the ouput \|\| error to the terminal                   | 'local',  's3' | 'local' |


   > **NOTE:** targets other than 'local' requires you to add the credentials in the config file
   

   <br>

   OUTPUT
{: .fs-6 .fw-300 }

   > does NOT return


---

</details>



<br>

---

<br>


### `Terminal_Task` class Attributes

* devices_dct
* connected_devices_dct
* inventory_groups
* *To be ogranized ...*

<br>