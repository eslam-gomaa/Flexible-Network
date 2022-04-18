---
layout: default
nav_order: 4
parent: Examples
title: 4. Test connection Management
markdown: Kramdown
kramdown:
  parse_block_html: true
  auto_ids: true
  syntax_highlighter: rouge
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


Script used in this example can be found in this directory: [Code Samples](https://github.com/eslam-gomaa/Flexible-Network/tree/develop/docs/code_samples)


**^ In this example we'll see what will happen if the connection is interrupted while the script is executing commands over the devices:**

As mentioned in the [concepts section](https://eslam-gomaa.github.io/Flexible-Network/concepts/#1-connection-management) the script authenticates ALL the devices of the selected group before it starts executing commands, so there is a possibility that a device's connection is interrupted due to different possible reasons {reboot, connection timeout, device went down, etc..}
* Before the execution of any command, the library checks if the ssh connection still active
    * And IF the ssh connection is NOT active, it tries to reconnect
        * If reconnected successfully, the library updates ssh connection information of the device & continue to execute normally.
        * If it's NOT able to reconnect, the command will return exit_code of `-1` 


---


<link rel="stylesheet" href="{{ site.baseurl }}/css/custom.css">

<script src="https://gist.github.com/eslam-gomaa/583b16cbf468ec90087aa9bb9441b839.js"></script>

---

## Test 1: the device went down during the execution.

### Run the script

```bash
python3.6 docs/Docs/Examples/sample-4.py -n task-4 --config ~/flexible_network.cfg  --inventory user/hots  --authenticate-group works --user orange --password cisco
```

### OUTPUT


{% highlight bash %}
> Authenticating selected devices
   90.84.41.239  [ 1 / 1 ]          Connected [ 1 ]     Failed [ 0 ]    

> Connection Report   
+--------------+---------------------+-----------+--------------+---------------+-------------------------+---------------+
| Host         | Connection Status   | Comment   |   N of tries |   Max Retries |   Time tring in seconds | Fail Reason   |
+==============+=====================+===========+==============+===============+=========================+===============+
| 90.84.41.239 | 🟢                  | connected |            1 |             3 |                       1 |               |
+--------------+---------------------+-----------+--------------+---------------+-------------------------+---------------+


WARNING -- Confirm before running the following command: 


enable
cisco
conf t
vlan 113
name Testing114
exit
exit
show vlan br 


yes || no 

yes: Run & continue
no:  Abort
YOUR Decision: yes
> Ok .. Let's continue ...


> 🟡 Closed Socket detected @90.84.41.239
> Trying to reconnect ...
> Authenticating selected devices
   90.84.41.239  [ 1 / 1 ]          Connected [ 0 ]     Failed [ 1 ]    
> 🔴 FAILED to reconnect to @90.84.41.239

@ 90.84.41.239
Execution Time: 16.32 seconds
enable
cisco
conf t
vlan 113
name Testing114
exit
exit
show vlan br 
{
    "cmd": [
        "enable",
        "cisco",
        "conf t",
        "vlan 113",
        "name Testing114",
        "exit",
        "exit",
        "show vlan br "
    ],
    "exit_code": -1,
    "stderr": [
        "Socket is closed > Failed to reconnect."
    ],
    "stdout": []
}


Socket is closed > Failed to reconnect.

> Stopped due to the previous error.
{% endhighlight %}


#### Screenshoots

![image](https://user-images.githubusercontent.com/33789516/163831159-85b89250-4600-458c-8680-cfbda91f50ed.png)

![image](https://user-images.githubusercontent.com/33789516/163831231-91d38a62-5560-4c2f-95ef-433a72bdd82d.png)


---

## Test 2: the device got rebooted || connection interrupted during the execution.


### Run the script

```bash
python3.6 docs/Docs/Examples/sample-4.py -n task-4 --config ~/flexible_network.cfg  --inventory user/hots  --authenticate-group works --user orange --password cisco
```

### OUTPUT


{% highlight bash %}
> Authenticating selected devices
   90.84.41.239  [ 1 / 1 ]          Connected [ 1 ]     Failed [ 0 ]    

> Connection Report   
+--------------+---------------------+-----------+--------------+---------------+-------------------------+---------------+
| Host         | Connection Status   | Comment   |   N of tries |   Max Retries |   Time tring in seconds | Fail Reason   |
+==============+=====================+===========+==============+===============+=========================+===============+
| 90.84.41.239 | 🟢                  | connected |            1 |             3 |                       1 |               |
+--------------+---------------------+-----------+--------------+---------------+-------------------------+---------------+


WARNING -- Confirm before running the following command: 


enable
cisco
conf t
vlan 113
name Testing114
exit
exit
show vlan br 


yes || no 

yes: Run & continue
no:  Abort
YOUR Decision: yes
> Ok .. Let's continue ...

Socket exception: Connection reset by peer (104)

> 🟡 Closed Socket detected @90.84.41.239
> Trying to reconnect ...
> Authenticating selected devices
   90.84.41.239  [ 1 / 1 ]          Connected [ 1 ]     Failed [ 0 ]    
> 🟢 Reconnected successfully to @90.84.41.239

@ 90.84.41.239
Execution Time: 1.9 seconds
enable
cisco
conf t
vlan 113
name Testing114
exit
exit
show vlan br 
{
    "cmd": [
        "enable",
        "cisco",
        "conf t",
        "vlan 113",
        "name Testing114",
        "exit",
        "exit",
        "show vlan br "
    ],
    "exit_code": 0,
    "stderr": [],
    "stdout": [
        "enable",
        "Password: ",
        "conf t",
        "Enter configuration commands, one per line.  End with CNTL/Z.",
        "vlan 113",
        "name Testing114",
        "exit",
        "exit",
        "show vlan br ",
        "VLAN Name                             Status    Ports",
        "---- -------------------------------- --------- -------------------------------",
        "1    default                          active    Et1/0, Et1/1, Et1/2, Et1/3",
        "11   mgmt                             active    Et0/0, Et0/2, Et0/3",
        "12   internal                         active    ",
        "13   testing                          active    ",
        "113  Testing114                       active    ",
        "123  testing123 TYPO2                 active    ",
        "1002 fddi-default                     act/unsup ",
        "1003 token-ring-default               act/unsup ",
        "1004 fddinet-default                  act/unsup ",
        "1005 trnet-default                    act/unsup "
    ]
}
{% endhighlight %}


#### Screenshoots

![image](https://user-images.githubusercontent.com/33789516/163832080-6dccd487-0bad-4980-876e-be4afbbafe95.png)

![image](https://user-images.githubusercontent.com/33789516/163832249-70418587-ecf1-45db-aa6c-2c13f0657316.png)

---

## Known issue

* When the device is reconnected you have to login to the enable mode again (and provide the enable secret)
* This will be considered in the next milestone

