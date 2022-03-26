# Flexible-Network

<br>

#### [ Under development ]


<br>

A Python library / tool to achieve advanced network automation scenarios with few lines of code
* Required: Basic python knowledge

A Refactored Version of [Flexible_Network  ((Proof of concept))  ](https://github.com/eslam-gomaa/Flexible_Network)

**BackLog**: https://flexible-network.devops-caffe.com

<br>

---

<br>

Before reading the features you need to know that the network devices are "dump", they don't detect errors (Just return outputs despite if it has an error or not), which limits the flexibility when using Python to automate them.


# Features

* Ability to detect errors when executing commands on network devices
   * When executing commands you get a `dict` of output similar to what you get when executing commands on Linux machines [check the `execute` method](#execute)
   * Which gives you the power to use ***Python conditionals*** when automating network devices. 

![image](https://user-images.githubusercontent.com/33789516/159186029-8f377b31-f839-40b6-96f6-33a6a42d5317.png)

* Multi-Vendor
   * Use a unified way to automate different types of devices from different vendors [ Check the list of supported vendors (_to be documented_) ]

* Backup config, with different storage options including `S3` [ Check the list of supported backup storage (_to be documented_) ]

* Integrations with different external APIs that gives more flexibility & efficiency to your scripts  [ Check the list of supported integrations (_to be documented_) ]


![image](https://user-images.githubusercontent.com/33789516/159433445-d040ce1a-752c-408b-b38e-1ea3ecb1e450.png)



<br>

---

<br>

# Install


## Install with `pip`

> **NOTE** At least Python3.6 is needed (_Dependencies constrains_)

```bash
# Will be published soon.
pip3.6 install FlexibleNetwork
```

<br>

> Download a sample `config file` & `inventory file`

```bash
mkdir /etc/flexible_network

# Download a sample hosts file
wget -O /etc/flexible_network/hosts https://raw.githubusercontent.com/eslam-gomaa/Flexible-Network/develop/user/hosts

# Download a sample config file
wget -O /etc/flexible_network/flexible_network.cfg https://raw.githubusercontent.com/eslam-gomaa/Flexible-Network/develop/user/flexible_network.cfg
```

<br>

<a id=--build-from-source></a>
## Build from source



Run unit tests
```bash
# Do NOT use it, deprecated  (Will be updated)
export PYTHONPATH=Flexible_Network/
python3.6 -m pytest tests/  -v
```

Build & Install
```bash 
git clone https://github.com/eslam-gomaa/Flexible-Network.git
cd Flexible-Network

# Build
python3.6 setup.py bdist_wheel
# Install
pip3.6 install dist/FlexibleNetwork-*.whl
   ```



<br>

After you have the library installed, you're ready to [use it](#_usage) !


<br>

---

<br>

# How it works !

* This project is designed as Python Library that you import to your Python script that gives you a lot of features and integrations out of the box
* After importing the library you can treat your script as a cli tool that  [[ Check the [cli parameters](#cli_options) ]] that you use to run tasks, get task logs, list & get backups etc.

> This section gives an overview of how the library works internally

<br>

### **. Inventory

We use the same inventory concept as Ansible, Here is an example of an inventory file

> This inventory has 4 groups works, `switches`, `routers`, `empty` each contains the devices listed below it

```ini
[works]
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

🟡 Custom inventory parameters will be added soon.





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


---


<br>

# Usage
<a id=_usage></a>

1. Create a new directory with a new Python script in it.

> The directory contains your python script is the project directory

```bash
mkdir sample-dir
cd sample-dir
touch my-network-script.py
```

<br>

2. import the `Terminal_Task` class from the `FlexibleNetwork` library & and instantiate an instance of the class

> open your script

```python
from FlexibleNetwork.Flexible_Network import Terminal_Task

# Instantiate an instance of the class 
## that represents a new task in the DB
task = Terminal_Task()

## Start using the available methods ..
```

3. Use the CLI to run the task ( Or list tasks/backups etc... )

```bash
python my-network-script.py -h
```

<br>

_From here, you can take a look at_ the complete examples ( _To be documented_ )

<br>

---

<br>

# Documentation

<a id=cli_options></a>
## Cli Options

<br>

### Run a task

<a id=--name></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--name</code></b>
  </summary>
  <br>
   The task name
   
   > *Required*
   
   > Each script run represents a task, Tasks state are stored.
</details>

<a id=--inventory></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--inventory</code></b>
  </summary>
  <br>
   file that contains the devices to automate
   
   > *Optional*
   
   > This argument overrides the following option in the config file.
   >```ini
   >[general]
   >default_inventory = /etc/flexible-network/hosts
   >```
</details>


<a id=--authenticate-group></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--authenticate-group</code></b>
  </summary>
  <br>
   Privide an inventory group to authenticate
   
   > *Optional*



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
</details>


<a id=--no-confirm-auth></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--no-confirm-auth</code></b>
  </summary>
  <br>
  Skip Asking for confirmation if failed to connect to some deivces
  
  > *Optional*

  > The dfault Behavior is to ask you for confirmation before proceeding if failed to authenticate to some devices.
</details>


<a id=--user></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--user</code></b>
  </summary>
  <br>
  The user to authenticate the group with

  > *Optional*
</details>


<a id=--password></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--password</code></b>
  </summary>
  <br>
  The password to authenticate the group with

  > *Optional*
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
   
   > *Optional*

   * ***Supported Options***'
        * `cyberArk`
        * `rocketChat`
        * `s3`
        * *more to be added soon*.
</details>



<br>

---

<br>

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
   | `terminal_print`       | str   | Print the ouput || error to the terminal                   | 'default',  'json' | 'default' |
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

 *Others To be documented*


<br>

---

<br>


### Supported API Integrations

<a id=rocketchat></a>
<details>
  <summary> 
  <b style="font-size:25px"> <code>RocketChat</code></b>
  </summary>
  <br>
  https://rocket.chat

  This integration allows you to send messages 

  #### Configuration section

  ```ini
  [rocket_chat]
   url      = https://******
   username = ******
   password = ******
  ```

  ##### Usage

  ```python
  from FlexibleNetwork.Integrations import RocketChat_API
  rocket = RocketChat_API()
  ```

  #### Methods

  * rocket.send_message()
  * _More to be documented_
  

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
<br>


---

<br>
<br>


### FAQs

<a id=faqs-execution-time></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>Why the execution time of a command takes around 0.4 ms at a minimum ?</code></b>
  </summary>
  <br>
   It takes much less than that, But we wait for a half a second before getting the result of a command from a device so that we're sure that we got the full output of the command

</details>


<a id=flexible-network-vs-ansible></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>Why to use this project while we can use Ansible for Network automation ?</code></b>
  </summary>
  <br>

  Ansible & Python have different ways for doing network automation

  <a id=flexible-network-vs-ansible></a>
   <details>
      <summary> 
      <b style="font-size:18px"> <code>How Ansible works for Network Automation.</code></b>
      </summary>
      <br>
   Yes, Ansible is idempotent with network automation

   > ***How does it work:***
      
   * Ansible uses modules, each vendor has different modules
   * At the begining of the automation task, Ansible gathers the running config of each device and parse, Hence when you tell it to create a VLAN for example, it first takes a look at the configuration it parsed before, and if the vlan does not exist, will create it.
      
   <br>
   <hr>
   <br>

   </details>


  But despite the different modules & features that ansible provides, many network engineers still prefer to use regular network commands for automation, and In fact Python is used extensively for network automation, **But the problem here** is that we can NOT easily achieve idempotency because network devices are DUMP!

  <br>

  And that's where the [Flexible-Network](https://github.com/eslam-gomaa/Flexible-Network#features) Project come into play.

  The most basic feature that our project gives you is the ability to deal with network devices the same way you used to deal with Linux machines  <sup>[1. Featues](https://github.com/eslam-gomaa/Flexible-Network#features)</sup>    <sup>[2. execute()](https://github.com/eslam-gomaa/Flexible-Network#execute)</sup>

   And that is not the only feature

  <br>

  **In short** [Flexible-Network](https://github.com/eslam-gomaa/Flexible-Network#features) `=>` (`simplicity` & `flexibility`) + `The Power of Python!` 💪

</details>


<br>
<br>
