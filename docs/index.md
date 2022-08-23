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

---

<br>

Before reading the features you need to know that the network devices are "dump", they don't detect errors (Just return outputs despite if it has an error or not), which limits the flexibility when using Python to automate them.


# Features

* Ability to detect errors when executing commands on network devices
   * When [executing commands](./Docs/usage/library_usage/class_methods.md#execute) you get output similar to what you get when executing commands on Linux machines
   * Which gives you the power to use ***Python conditionals*** when automating network devices. 

![image](https://user-images.githubusercontent.com/33789516/159186029-8f377b31-f839-40b6-96f6-33a6a42d5317.png)

* Multi-Vendor
   * Use a unified way to automate different types of devices from different vendors [ [Suppoerted vendors](./Docs/supported-vendors/supported-vendors.md) ]

* Backup config, with different storage options including `local storage` & `S3` (any S3 compatable object storage) [ [supported backup storage] ](./Docs/ConfigBackup-storage/backup_config-storage.md)

* Integrations with different external APIs that gives more flexibility & efficiency to your scripts  [ [Supported integrations] ](./Docs/Integrations/integrations.md)


![image](https://user-images.githubusercontent.com/33789516/159433445-d040ce1a-752c-408b-b38e-1ea3ecb1e450.png)


---


## FAQs

<details markdown="1" id="faqs-execution-time">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>Why the execution time of a command takes around 0.6 ms ?</code></b>
  </summary>
   It takes much less than that, But we wait for a half a second before getting the result of a command from a device so that we're sure that we got the full output of the command

</details>


<details markdown="1" id="flexible-network-vs-ansible">
  <summary markdown='span'> 
  <b style="font-size:20px"> <code>Why to use <b>Flexible-Network</b> while we can use Ansible for Network automation ?</code></b>
  </summary>

  Ansible and Flexible-Network have different ways of work
  - Ansible requires you to use Modules for the vendor you want to automate, and just running commands with ansible will not give you any fancy feature (no error detection).
  - Flexible-Network focuses on powering the network automation with Python, allows you to make productive network automation scripts with simple python code.
    - Use the same automation method for different types of vendors
    - Just use the commands you use for automation !  (no need different Modules syntax)
    - Focues on Network automation simplicy and productivity, [supported backup storage](./Docs/ConfigBackup-storage/backup_config-storage.md)  [ [Supported integrations] ](./Docs/Integrations/integrations.md) [Usage](./Docs/usage/usage.md)


</details>


---

#### The contributors of Flexible-Network!

<ul class="list-style-none">
{% for contributor in site.github.contributors %}
  <li class="d-inline-block mr-1">
     <a href="{{ contributor.html_url }}"><img src="{{ contributor.avatar_url }}" width="32" height="32" alt="{{ contributor.login }}"/></a>
  </li>
{% endfor %}
</ul>
