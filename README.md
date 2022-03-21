# Flexible-Network

<br>

#### [ Under development ]


Dev branch

<br>

A Python library / tool to achieve advanced network automation scenarios with few lines of code
* Required: Basic python knowledge

This is a Refactored Version of [Flexible_Network  ((Proof of concept))  ](https://github.com/eslam-gomaa/Flexible_Network)

**BackLog**: https://flexible-network.devops-caffe.com

<br>

---

<br>

Before reading the features you need to know that the network devices are "dump", they don't detect errors (Just return outputs despite if it has an error or not), which limits the flexibility when using Python to automate them.


# Features

* Ability to detect errors when executing commands on network devices
* When executing commands you get a `dict` of output similar to what you get when executing commands on Linux machines [check the `execute` method](#execute)
   * Which gives you the power to use ***Python conditionals*** when automating network devices. 
* *To be documented ...*

![image](https://user-images.githubusercontent.com/33789516/159186029-8f377b31-f839-40b6-96f6-33a6a42d5317.png)



<br>

---

<br>

# Install

> **NOTE** At least Python3.6 is needed (_Dependencies constrains_)

```bash
# Will be published soon.
pip3.6 install FlexibleNetwork
```

<br>

#### Build from source

```bash 
git clone https://github.com/eslam-gomaa/Flexible-Network.git
cd Flexible-Network

python3.6 setup.py bdist_wheel
pip3.6 install dist/FlexibleNetwork-*.whl
```


_Unit testing [ Ignore it for now ]_
```bash
# Do NOT use it, deprecated  (Will be updated)
export PYTHONPATH=Flexible_Network/
python3.6 -m pytest tests/  -v
```

<br>

After you have the library installed, you're ready to [use it](#_usage) !


<br>

---

<br>

# How it works !

* This project is designed as Python Library that you import to your Python script that gives you a lot of features and integrations out of the box
* After importing the library you can treat your script as a cli tool
* 

### 1. Connection Management

This project uses SSH to connect to the devices

**The way it works:** it tries to connect to the selected group of devices, and store the `ssh Channels` of the connected devices in a dictionary [ Which you have access to when you create an instance of the class ]

So in simple words, it opens the ssh connection with ALL the selected devices before start executing commands.

And that actually gives us more flexibility from the development perspective, besides *it's much better to be notified if you're NOT able to connect to some devices before starting the automation task* rather than being told at the end of task.


![image](https://user-images.githubusercontent.com/33789516/159185347-bbee6112-39e8-4818-93a3-9cea1946fcd1.png)





<br>

---

<br>

# Usage
<a id=_usage></a>

```bash
python <your-script.py> -h
```

<br>

---

<br>

# Documentation


### Cli Options

<br>

#### Run a task

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

#### get tasks

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


<a id=execute></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>execute()</code></b>
  </summary>
  Execute a command on a remote device.

<br>
<br>

> Returns a dictionary

|  Key           | Type   | Description                                                  |
| ----------- | ------ | ------------------------------------------------------------ |
| `stdout`    | List   | List of lines [ The output of the command ( If any ) ]           |
| `stderr`    | List   | List of lines [ The error of the command ( If any ) ]                  |
| `exit_code` | Int    | - `0` The command executed successfully<br />- `1` The command executed with an error <br />- `-1` If the ssh channel was interrupted while excution. 

* **Input**
   1. The ssh channel of the device
   2. The command to execute

**Sample Output**

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

### `Terminal_Task` class Attributes

* devices_dct
* connected_devices_dct
* inventory_groups
* *To be ogranized ...*

<br>
<br>
<br>
<br>
<br>




