---
layout: default
nav_order: 2
parent: Examples
title: 2. Take config backup
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

Script used in this example can be found in this directory: [Examples](https://github.com/eslam-gomaa/Flexible-Network/tree/develop/docs/Docs/Examples)


In this example we create a script that does the following:
1. Authenticate to the selected [inventory](https://eslam-gomaa.github.io/Flexible-Network/inventory) group (Using CLI)
2. [execute ](https://eslam-gomaa.github.io/Flexible-Network/terminal_class_methods#execute) set of commands
3. [Take a config backup](https://eslam-gomaa.github.io/Flexible-Network/Docs/ConfigBackup-storage/config-backup-storage/) & store it in S3


---

<script src="https://gist.github.com/eslam-gomaa/4fdfc5e4fb21a2c562b4e47830db8f72.js"></script>

---

### Run the script

```bash
python3.6 docs/Docs/Examples/sample-2.py -n task-1 --config ~/flexible_network.cfg  --inventory user/hots  --authenticate-group works --user orange --password cisco
```

#### OUTPUT


```bash
> Authenticating selected devices
   90.84.41.239  [ 1 / 1 ]          Connected [ 1 ]     Failed [ 0 ]    

> Connection Report   
+--------------+---------------------+-----------+--------------+---------------+-------------------------+---------------+
| Host         | Connection Status   | Comment   |   N of tries |   Max Retries |   Time tring in seconds | Fail Reason   |
+==============+=====================+===========+==============+===============+=========================+===============+
| 90.84.41.239 | 🟢                  | connected |            1 |             3 |                       1 |               |
+--------------+---------------------+-----------+--------------+---------------+-------------------------+---------------+


@ 90.84.41.239
Execution Time: 0.5 seconds
sh ip int br
Interface              IP-Address      OK? Method Status                Protocol
Ethernet0/0            unassigned      YES unset  up                    up      
Ethernet0/1            unassigned      YES unset  up                    up      
Ethernet0/2            unassigned      YES unset  up                    up      
Ethernet0/3            unassigned      YES unset  up                    up      
Ethernet1/0            unassigned      YES unset  up                    up      
Ethernet1/1            unassigned      YES unset  up                    up      
Ethernet1/2            unassigned      YES unset  up                    up      
Ethernet1/3            unassigned      YES unset  up                    up      
Vlan1                  unassigned      YES unset  administratively down down    
Vlan11                 192.168.11.2    YES NVRAM  up                    up      
backup-config-eslam-5

@ 90.84.41.239
> backup taken successfully > [ Testing S3 integrations ]
```

---

#### Screenshoots


![image](https://user-images.githubusercontent.com/33789516/163047768-910992cd-035d-4996-8198-d11c294ccdca.png)


---

### List the backups

```bash
python3.6 docs/Docs/Examples/sample-2.py --backup --list
```

{% highlight bash %}
| a893500c-836e-4d22-94b9-e4980be1fe00 | Testing S3 integrations  | 90.84.41.239 | s3       | 🟢 success | 29-03-2022 | 10-47-05 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
| 4d6fae23-8c80-417a-bafb-af617b6dd5ba | test                     | 90.84.41.239 | local    | 🔴 failed  | 01-04-2022 | 06-10-32 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
| 41ce52a6-0c03-4efe-a29d-07ef752c53f0 | test                     | 90.84.41.239 | local    | 🟢 success | 01-04-2022 | 06-13-12 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
| e02e2910-c3b3-4e25-9f1c-19fa389f1710 | test                     | 90.84.41.239 | local    | 🟢 success | 01-04-2022 | 06-14-09 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
| 116ba93e-4e90-4e33-9b39-0b89b37e648e | test                     | 90.84.41.239 | local    | 🟢 success | 01-04-2022 | 06-14-32 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
| 53a63787-6f26-4d23-89c5-18a71471bc50 | Testing S3 integrations  | 90.84.41.239 | s3       | 🟢 success | 12-04-2022 | 20-25-50 |
+--------------------------------------+--------------------------+--------------+----------+------------+------------+----------+
{% endhighlight %}


![image](https://user-images.githubusercontent.com/33789516/163048128-21054160-d338-4475-8711-766942cdf62d.png)


---


### Get the backup



![image](https://user-images.githubusercontent.com/33789516/163049335-7dfcfc02-302c-4601-a4d0-45dce0796e66.png)

**Note:** For any backup targets other than `local` you need to specify the configuration file. _(which in this case contains the credentials for S3 APIs)_

![image](https://user-images.githubusercontent.com/33789516/163049627-a5ec7962-8fbf-487b-bcd9-1ac9a146cc6c.png)