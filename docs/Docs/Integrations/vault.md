---
layout: default
nav_order: 3
# permalink: /integrations/cyberark
parent: Integrations
title: Vault
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

Allows you to get/update secrets from & to Vault secret manager.
{: .fs-6 .fw-300 }

[**https://www.vaultproject.io**](https://www.vaultproject.io){: .btn }


<br>

To be supported in [0.4.0 release](https://github.com/users/eslam-gomaa/projects/2/views/1)