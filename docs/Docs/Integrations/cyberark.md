---
layout: default
nav_order: 2
# permalink: /integrations/cyberark
parent: Integrations
title: CyberArk
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

# CyberArk
{: .fs-9 }

Allows you to get/update credentials from & to Cyberark secret manager.
{: .fs-6 .fw-300 }

[**https://www.cyberark.com**](https://www.cyberark.com){: .btn }


To be documented

```
{% raw %}
**Note**
{% endraw %}
```