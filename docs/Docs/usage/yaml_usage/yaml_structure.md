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


### Task.subTask.authenticate

```yaml
Task:
  name: New Task
  log_format: markdown
  subTask:
    - name: Love forever
      vendor: cisco
      parallel: false
      authenticate:
        group: switches
        port: 22
        username:
          value_from_env:
            key: my_username
        password:
          value_from_env:
            key: my_password
        privileged_mode_password:
          value_from_env:
            key: my_password
        reconnect: True
```

| Input                      | Type    | Description                                                  | Options         | Default |
| -------------------------- | ------- | ------------------------------------------------------------ | --------------- | ------- |
| `group`                    | String  | Inventory group to authenticate                              |                 |         |
| `port`                     | Integer |                                                              |                 | 22      |
| username                   | dct     | Username for authentication                                  |                 |         |
| password                   | dct     | Password for authentication                                  |                 |         |
| `privileged_mode_password` | dct     | Password of the Privileged mode (eg. `enable` in Cisco & `super` in Huawei) [ *If Provided, the device login to `privileged_mode` after authentication.* ] |                 |         |
| reconnect                  | Boolan  | Wheather to reconnect if the SSH connection is interupted    | `True`, `False` | False   |
|                            |         |                                                              |                 |         |

> For options with `dct` type

#### Provide value directly

```yaml
username:
  value: Trump
```

#### Provide value from ENV

```yaml
username:
  value_from_env:
    key: my_username
```

* Providing values from Secret managers like Vault & Cyberark, will be considered in [0.4.0 release](https://github.com/eslam-gomaa/Flexible-Network/milestone/2)




<br>

---

<br>

