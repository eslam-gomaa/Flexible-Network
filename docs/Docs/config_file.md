
---
layout: default
permalink: /
title: Config file
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


# Configuration file

The configuration file is used mainly to provide credentials for the external APIs like `S3`, `CyberArk`, etc. 

> **Note:** Reading credentials from Environment Variables will be considered in the next milestone.

<br>

The default location of the configuration file is expected at `/etc/flexible_network/flexible_network.cfg` 

<br>

To provide a custom config file location you can use the `--config` or `-c` CLI option 

<a id=sample_config_file></a>
<br>

**Sample configuration file**

```ini
[general]
default_inventory = /etc/flexible-network/hosts

[cyberark]m
url      = https://your-cyberark-server.com
username = **********
password = **********
verify_ssl = False
concurrent_session = True
authentication_method = 'LDAP'


[rocket_chat]
url      = https://your-rocket-chat-server.com
username = **********
password = **********


[s3]
# Endpoint of Flexible Engine (Openstack based public cloud platform)
endpoint = "https://oss.eu-west-0.prod-cloud-ocb.orange-business.com"
ak       = "**********"
sk       = "**********"
region   = "default"
# region   = "eu-west-0"
bucket   = 'backup-config-eslam-5'
# Create the bucket if does NOT exist
create_bucket = True
```

