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