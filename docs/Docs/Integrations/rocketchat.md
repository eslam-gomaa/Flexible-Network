---
layout: default
nav_order: 1
# permalink: /integrations/rocketchat
parent: Integrations
title: RocketChat
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


https://rocket.chat

This integration allows you to send messages & attachments to RocketChat users & channels

#### Configuration section

```ini
[rocket_chat]
url      = https://your-rocket-chat-server.com
username = **********
password = **********
```

[A full config file sample](/Docs/config_file.md#sample_config_file)

##### Usage

```python
from FlexibleNetwork.Integrations import RocketChat_API
rocket = RocketChat_API()
```

#### Methods


<a id=send_message()></a>
<details>
  <summary> 
  <b style="font-size:20px"> <code>send_message()</code></b>
  </summary>
  <br>
  Allows you to send a RocketChat message to a list of users

   ### INPUT

   | Input     | Type | Description                                                  | Options        | Default |
   | --------- | ---- | ------------------------------------------------------------ | -------------- | ------- |
   | `member_name_lst` | List of strings  | users to send messages to.     |                |         |
   | `message` | String  | Message to send                |                |         |

   ### OUTPUT

   > Returns a dictionary

   | Key     | Type | Description                                                  | Options        | Default |
   | --------- | ---- | ------------------------------------------------------------ | -------------- | ------- |
   | `success` | Boolean  | Whether the message was sent successfully or not.     |                |         |
   | `fail_reason` | String  | Message to send                |                |         |




</details>

Other methods to be documented.