# Flexible-Network

<br>

#### [ Under development ]


<br>

A Python library / tool to achieve advanced network automation scenarios with few lines of code
* Required: Basic python knowledge

This is a Refactored Version of [Flexible_Network  ((Proof of concept))  ](https://github.com/eslam-gomaa/Flexible_Network)

Our collaboration page: https://flexible-network.devops-caffe.com

<br>

---

<br>

# Features
* Ability to detect errors when executing commands on network devices
* When executing commands you get a `dict` of output similar to what you get when executing commands on Linux machines [check the `exec` method](#exec)
   * Which gives you the power to use ***Python conditionals*** when automating network devices. 
* ... To be documented



<br>

---

<br>

# Install

#### Will be available to install as a Python Library

> **NOTE** At least Python3.6 is needed (_Dependencies constrains_)

```bash
pip3.6 install ... # Soon
```

<br>

#### Build

Install libraries dependencies

```
pip3.6 install --user -r  Flexible_Network/requirements.txt
```

```bash
# Do NOT use it, deprecated  (Will be updated)
export PYTHONPATH=Flexible_Network/
python3.6 -m pytest tests/  -v
```

```
# Soon
```


<br>

---

<br>

# Usage

* This project is designed as Python Library that you import to your Python script that gives you a lot of features and integrations out of the box
* After importing the library you can treat your script as a cli tool
* 

```bash
python <your-script.py> -h
```

<br>

---

<br>

# Documentation


### Cli Options

[test](#--authenticate-group)

* `--name`
The task name
> Each script run represents a task, Tasks state are stored.

* `--inventory`
file that contains the devices to automate

* `--validate-integration`
Validate the integration with any of the supported API Integrations eg. test to authenticate (And validate permissions if needed).

* `--no-confirm-auth`
Skip asking for confirmation if failed to authenticate to some devices.



<a id=--authenticate-group></a>
<br>
<details>
  <summary> 
  <b style="font-size:20px"> <code>--authenticate-group</code></b>
  </summary>
   Privide an inventory group to authenticate



> **Note:** this option requires to specify the `--user` & `--password` arguments 

> Example
```bash
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










<br>

---

<br>

### `Terminal_Task` class Methods

```python
from Flexible_Network import Terminal_Task
```


<a id=exec></a>
<details>
<a id=exec></a>
  <summary> 
  <b style="font-size:20px"> <code>exec()</code></b>
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


<br>

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

 Others To be documented



<br>
<br>
<br>
<br>
<br>



