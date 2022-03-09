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


Returns a dictionary

|             | Type   | Description                                                  |
| ----------- | ------ | ------------------------------------------------------------ |
| `stdout`    | String | The output of the command (I f any )                         |
| `stderr`    | String | The error of the command ( If any )                          |
| `exit_code` | Int    | - `0` The command executed successfully<br />- `1` The command executed with an error <br />- `-1` If the ssh channel was interrupted while excution. 


</details>





