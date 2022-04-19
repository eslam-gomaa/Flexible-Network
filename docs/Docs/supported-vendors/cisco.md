---
layout: default
nav_order: 1
parent: Supported Vendors
title: Cisco
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

# Cisco
{: .fs-9 }

To set the vendor to Cisco
{: .fs-6 .fw-300 }


```python
from FlexibleNetwork.Vendors import Cisco

task.vendor = Cisco()
```