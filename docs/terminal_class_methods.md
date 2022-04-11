---
layout: default
nav_order: 4
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


### `Terminal_Task` class Methods

```python
from Flexible_Network import Terminal_Task
```

<a id=authenticate></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>authenticate</code></b>
  </summary>
  <br>
   Authenticate with an inventory group

  ***Note:*** You can access the inventory through the `inventory_groups` attribute.
  > **`inventory_groups`** is a dictionary where its keys are the inventory groups

  Example on authenticating with the `all` group which contains all the hosts from all the groups
  ```python
  task.authenticate(hosts=task.inventory_groups['all'], user='orange', password='cisco', port='1113')
  ```

  * The `authentication` method will update the `devices_dct` & `connected_devices_dct` attributes
    * `devices_dct` `->` A dictionary, contains all the hosts of the authenticated group including the ones that failed to authenticate [ each key is the host IP & the value is the host info ]
    * `connected_devices_dct` -> the same as `devices_dct` but only contains the authenticated hosts.


</details>


<a id=execute_raw></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>execute_raw()</code></b>
  </summary>

  Execute a command on a remote device.

   <br>

  > **Note:** This method does not print to the terminal.
  
<br>

### INPUT

|  Input      | Type       | Description                                                  |
| ----------- | ------     | ------------------------------------------------------------ |
| `hos_dct`   | dictionary | The host dictionary => is key of the  `connected_devices_dct` attribute  (And contains information about the device including the `ssh channel` to use for the command execution )   |
| `cmd`       | string     | The command to run on the remote device                |

<br>

### OUTPUT

> Returns a dictionary

|  Key           | Type   | Description                                                  |
| ----------- | ------ | ------------------------------------------------------------ |
| `stdout`    | List   | List of lines [ The output of the command ( If any ) ]           |
| `stderr`    | List   | List of lines [ The error of the command ( If any ) ]                  |
| `exit_code` | Int    | - `0` The command executed successfully<br />- `1` The command executed with an error <br />- `-1` If the ssh channel was interrupted during excution. 



<br>

**Sample Output**

Sample of a successful command

```json
{
   "cmd":[
      "sh ip int br"
   ],
   "stdout":[
      "Interface              IP-Address      OK? Method Status                Protocol",
      "Ethernet0/0            unassigned      YES unset  up                    up      ",
      "Ethernet0/1            unassigned      YES unset  up                    up      ",
      "Ethernet0/2            unassigned      YES unset  up                    up      ",
      "Ethernet0/3            unassigned      YES unset  up                    up      ",
      "Ethernet1/0            unassigned      YES unset  up                    up      ",
      "Ethernet1/1            unassigned      YES unset  up                    up      ",
      "Ethernet1/2            unassigned      YES unset  up                    up      ",
      "Ethernet1/3            unassigned      YES unset  up                    up      ",
      "Vlan1                  unassigned      YES unset  administratively down down    ",
      "Vlan11                 192.168.11.2    YES NVRAM  up                    up      "
   ],
   "stderr":[],
   "exit_code":0
}
```

Sample of an unsuccessfull command

```json
{
   "cmd":[
      "sh ip int br Typo"
   ],
   "stdout":[
      "                      ^",
      "% Invalid input detected at '^' marker."
   ],
   "stderr":[
      "sh ip int br Typo",
      "                      ^",
      "% Invalid input detected at '^' marker.",
      "mgmt_sw>",
      "mgmt_sw>",
      "mgmt_sw>"
   ],
   "exit_code":1
}
```

Sample of an unsuccessfull command ( Connection closed before or during the execution )


```json
{
   "cmd":[
      "sh ip int br Typo"
   ],
   "stdout":[],
   "stderr":[
      "Socket is closed"
   ],
   "exit_code":-1
}
```
</details>


<a id=execute></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>execute()</code></b>
  </summary>

  Execute a command on a remote device.

   <br>

  > **Note:** This method prints the output to the terminal.
   
   <br>

   ### INPUT


   | Input                  | Type  | Description                                                  | Options            | Default   |
   | ---------------------- | ----- | ------------------------------------------------------------ | ------------------ | --------- |
   | `hos_dct`              | dct   | The host dictionary => is key of the  `connected_devices_dct` attribute  (And contains information about the device including the `ssh channel` to use for the command execution ) |                    |           |
   | `cmd`                  | str   | The command to run on the remote device                      |                    |           |
   | `terminal_print`       | str   | Print the ouput \|\| error to the terminal                   | 'default',  'json' | 'default' |
   | `ask_for_confirmation` | bool  | Ask for confirmation before executing a command,             |                    | False     |
   | `exit_on_fail`         | boola | Exit the script with code of `1` if the command executed with errors |                    | True      |

   <br>

   ### OUTPUT

   > Returns a dictionary

   |  Key           | Type   | Description                                                  |
   | ----------- | ------ | ------------------------------------------------------------ |
   | `stdout`    | List   | List of lines [ The output of the command ( If any ) ]           |
   | `stderr`    | List   | List of lines [ The error of the command ( If any ) ]                  |
   | `exit_code` | Int    | - `0` The command executed successfully<br />- `1` The command executed with an error <br />- `-1` If the ssh channel was interrupted during excution. 

### Sample Output

[The same as `execute_raw` method](#execute_raw)


</details>


<a id=execute_from_file></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>execute_from_file()</code></b>
  </summary>

  Load commands from file & execute each line one by one. using the [execute()](#excute) method

   <br>

  > **Note:** This method prints the output to the terminal.
   
   <br>

   ### INPUT


   | Input                  | Type  | Description                                                  | Options            | Default   |
   | ---------------------- | ----- | ------------------------------------------------------------ | ------------------ | --------- |
   | `hos_dct`              | dct   | The host dictionary => is key of the  `connected_devices_dct` attribute  (And contains information about the device including the `ssh channel` to use for the command execution ) |                    |           |
   | `file`                 | str   | The file to load the commands from                      |                    |           |
   | `terminal_print`       | str   | Print the ouput \|\| error to the terminal                   | 'default',  'json' | 'default' |
   | `ask_for_confirmation` | bool  | Ask for confirmation before executing a command,             |                    | False     |
   | `exit_on_fail`         | boola | Exit the script with code of `1` if the command executed with errors |                    | True      |


   <br>

   ### OUTPUT

   > does NOT return

</details>


<a id=connection_report_Table></a>
<details>
  <summary> 
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


</details>


<a id=backup_config></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>backup_config()</code></b>
  </summary>

  Backup running configuration from the remote device & store them in the local directory by default, for other backup storage options check [supported backup targets]

   <br>

  > **Note:** This method prints the output to the terminal.
   
   <br>

   ### INPUT

   | Input     | Type | Description                                                  | Options        | Default |
   | --------- | ---- | ------------------------------------------------------------ | -------------- | ------- |
   | `hos_dct` | dct  | The host dictionary => is key of the  `connected_devices_dct` attribute  (And contains information about the device including the `ssh channel` to use for the command execution ) |                |         |
   | `comment` | str  | A comment indicates the purpose of the backup                |                |         |
   | `target`  | str  | Print the ouput \|\| error to the terminal                   | 'local',  's3' | 'local' |


   > **NOTE:** targets other than 'local' requires you to add the credentials in the config file
   

   <br>

   ### OUTPUT

   > does NOT return

</details>



<br>

---

<br>

---

<br>


### `Terminal_Task` class Attributes

* devices_dct
* connected_devices_dct
* inventory_groups
* *To be ogranized ...*

<br>
<br>


---

<br>
<br>

