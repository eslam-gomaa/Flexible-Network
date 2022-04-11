---
layout: default
nav_order: 2
parent: Home
title: Installation
markdown: Kramdown
kramdown: 2
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

# Installation
{: .fs-9 }


## Install with `pip`

> **Note** At least Python3.6 is needed (_Dependencies constrains_)
{: .fs-2 .fw-300 }


[**view on pypi.org**](https://pypi.org/project/FlexibleNetwork){: .btn }



```bash
pip3.6 install FlexibleNetwork
```

<br>

☝️ Download a sample `config file` & `inventory file`

```bash
mkdir /etc/flexible_network

# Download a sample hosts file
wget -O /etc/flexible_network/hosts https://raw.githubusercontent.com/eslam-gomaa/Flexible-Network/develop/user/hosts

# Download a sample config file
wget -O /etc/flexible_network/flexible_network.cfg https://raw.githubusercontent.com/eslam-gomaa/Flexible-Network/develop/user/flexible_network.cfg
```

<br>

---


## Build from source



Run unit tests
```bash
# Do NOT use it, deprecated  (Will be updated)
export PYTHONPATH=Flexible_Network/
python3.6 -m pytest tests/  -v
```

Build & Install
```bash 
git clone https://github.com/eslam-gomaa/Flexible-Network.git
cd Flexible-Network

# Build
python3.6 setup.py bdist_wheel
# Install
pip3.6 install dist/FlexibleNetwork-*.whl
   ```



<br>

After you have the library installed, you're ready to [use it](#_usage) !


<br>
