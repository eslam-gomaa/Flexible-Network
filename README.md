# Flexible-Network

Building on https://github.com/eslam-gomaa/Flexible_Network

Our collaboration page: https://flexible-network.devops-caffe.com

<br>

---


#### Install

> **NOTE** At least Python3.6 is needed

Install libraries dependencies

```
pip3.6 install --user -r  Flexible_Network/requirements.txt
```



#### Run unit tests

```
# Do NOT use it, deprecated
export PYTHONPATH=Flexible_Network/
python3.6 -m pytest tests/  -v
```

<br>

---

<br>

## Documentation

### Methods

<details>
  <summary> <code>.exec()</code> </summary>
  Execute a command on a remote device.

<br>
<br>

> Returns a dictionary

|             | Type   | Description                                                  |
| ----------- | ------ | ------------------------------------------------------------ |
| `stdout`    | String | The output of the command (I f any )                         |
| `stderr`    | String | The error of the command ( If any )                          |
| `exit_code` | Int    | - `0` The command executed successfully<br />- `1` The command executed with an error <br />- `-1` If the ssh channel was interrupted while excution. 

**Sample Output**

```json
{
   "cmd":[
      "sh ip int br"
   ],
   "stdout":"",
   "stderr":"Socket is closed",
   "exit_code":-1
}
```

```json
{
   "cmd":[
      "sh ip int br",
      ""
   ],
   "stdout":"sh ip int br\r\nInterface              IP-Address      OK? Method Status                Protocol\r\nEthernet0/0            unassigned      YES unset  up                    up      \r\nEthernet0/1            unassigned      YES unset  up                    up      \r\nEthernet0/2            unassigned      YES unset  up                    up      \r\nEthernet0/3            unassigned      YES unset  up                    up      \r\nEthernet1/0            unassigned      YES unset  up                    up      \r\nEthernet1/1            unassigned      YES unset  up                    up      \r\nEthernet1/2            unassigned      YES unset  up                    up      \r\nEthernet1/3            unassigned      YES unset  up                    up      \r\nVlan1                  unassigned      YES unset  administratively down down    \r\nVlan11                 192.168.11.2    YES NVRAM  up                    up      \r\nmgmt_sw>\r\nmgmt_sw>\r\nmgmt_sw>",
   "stderr":"",
   "exit_code":0
}
```

</details>





