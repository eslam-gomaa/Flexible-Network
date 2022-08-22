---
layout: default
nav_order: 2
# parent: Home
title: Usage
markdown: Kramdown
has_children: true
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

####  USAGE
{: .fs-6 .fw-300 }
{: .no_toc }

<br>

There are 2 ways to use Flexible Network:
{: .fs-6 .fw-300 }

- [As a Python Library](./library.md) (Use its functions within your Python script)
- [Use YAML manifests as Input](./yaml_manifest.md) (No coding is required) 


---

#### General
{: .fs-6 .fw-300 }
- You need the add the hosts you'll automate in an [inentory file](../inventory.md)
- If you plan to use any of the external APIs, make sure you put their connection options in the [config file](../config_file.md)
