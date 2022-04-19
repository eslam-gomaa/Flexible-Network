---
layout: default
nav_order: 2
parent: Supported Vendors
title: Huawei
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


# Huawei
{: .fs-9 }

To set the vendor to Huawei
{: .fs-6 .fw-300 }


```python
from FlexibleNetwork.Vendors import Huawei

task.vendor = Huawei()
```

[Full Example](https://eslam-gomaa.github.io/Flexible-Network/Docs/Examples/example-5/)

