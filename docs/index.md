---
# default, page
layout: default
nav_order: 1
description: A Python library / cli-tool to achieve advanced network automation scenarios with few lines of code
permalink: /
title: Home
has_children: true
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

# Flexible Network documentation
{: .fs-9 }


A Python library / cli-tool to achieve advanced network automation scenarios with few lines of code
{: .fs-6 .fw-300 }

[Get started now](#features){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [View it on GitHub](https://github.com/eslam-gomaa/Flexible-Network){: .btn .fs-5 .mb-4 .mb-md-0 }


<br>

<!-- <details markdown="1" id="toc">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>Table of contents</code></b>
  </summary>

- TOC
{:toc}

</details> -->

1. TOC
{:toc}

<br>
A Refactored Version of [Flexible_Network  ((Proof of concept))  ](https://github.com/eslam-gomaa/Flexible_Network)


[ Under development ]

[**BackLog**](https://shiny-pruner-f62.notion.site/Flexible-Network-Project-8a037585793a4405acf892e66e6a4132){: .btn }


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


---


## FAQs

<details markdown="1" id="faqs-execution-time">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>Why the execution time of a command takes around 0.6 ms ?</code></b>
  </summary>
  <br>
   It takes much less than that, But we wait for a half a second before getting the result of a command from a device so that we're sure that we got the full output of the command

</details>


<details markdown="1" id="flexible-network-vs-ansible">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>Why to use this project while we can use Ansible for Network automation ?</code></b>
  </summary>
  <br>

  Ansible & Python have different ways for doing network automation

   <details markdown="1" id="flexible-network-vs-ansible">
      <summary markdown='span'>
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


