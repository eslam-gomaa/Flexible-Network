---
layout: default
nav_order: 2
parent: Python Library
grand_parent: Usage
title: Terminal_Class options
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


# `Terminal_Task` class Options
{: .fs-9 }

<br>


#### task_log_formate
{: .fs-6 .fw-300 }


| Input             | Type   | Description          | Options            | Default    |
| ----------------- | ------ | -------------------- | ------------------ | ---------- |
| `task_log_formate` | String | Task log file format | `markdown`,  `txt` | `markdown` |

> **Note:** Markdown format provides a pretty looking for Task log, but it may be a put some extra load for the Terminal app to display it, if log looking doesn't matter to you, you can use the "txt" log format.


```python
from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Vendors import Cisco

task = Terminal_Task(task_log_format="txt")
```



---

<br>
