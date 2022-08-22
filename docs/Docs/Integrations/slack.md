---
layout: default
nav_order: 4
# permalink: /integrations/cyberark
parent: Integrations
title: Slack
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

Allows you to send messages & attachments to Slack users & channels
{: .fs-6 .fw-300 }

[**https://slack.com**](https://slack.com){: .btn }


<br>

To be supported in [0.4.0 release](https://github.com/eslam-gomaa/Flexible-Network/milestone/2)