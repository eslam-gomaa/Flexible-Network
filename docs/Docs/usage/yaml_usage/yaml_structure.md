---
layout: default
nav_order: 1
parent: YAML Manifest
grand_parent: Usage
title: YAML Structure
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

<br>

# YAML Structure
{: .fs-9 }

<br>


- Each YAML document contains a Task
  - Each task contains sub-Tasks
    - Each sub-Task contains number of functions like `execute`, `take_config_backup` etc.



#### 1. Create a new Task
{: .fs-6 .fw-300 }


```yaml
Task:
  name: New Task
  log_format: markdown
  subTask:
    - name: Love forever
      vendor: cisco
      parallel: false
```

### Task

| Input                 | Type   | Description                                                  | Options             | Default    |
| --------------------- | ------ | ------------------------------------------------------------ | ------------------- | ---------- |
| `task_log_format`     | String | Task log file format                                         | `markdown`,  `txt`  | `markdown` |
| `task_name`           | String | The name of the task (which will be displayed when listing tasks) |                     |            |
| `Task.subTask`        | List   | List of subtasks (will be executed in order)                 |                     |            |
| `Task.subTask.name`   | String | Name of sub-task                                             |                     |            |
| `Task.subTask.vendor` | String | Default Vendor for the sub-task                              | `cisco`,   `huawei` | `cisco`    |
| Task.subTask.parallel | Boolan | Wheather to execute the sub-task on the devices in Parallel, _Currently not supported, will be supported in an upcoming release_ | `True`, `False`     | False      |
|                       |        |                                                              |                     |            |

### subTask






Alternative to set the task name as a class Parameter, is to provid it as a CLI argument

```bash
python3 <your script>.py --name "Test task 2"
```

> **NOTE** The cli provided task name takes effect if both ways are used together.


```python
from FlexibleNetwork.Flexible_Network import Terminal_Task
from FlexibleNetwork.Vendors import Cisco

task = Terminal_Task(task_log_format="txt")
```


<br>

---

<br>

