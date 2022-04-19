---
layout: default
nav_order: 5
parent: Examples
title: 5. Use different vendors
markdown: Kramdown
kramdown:
  parse_block_html: true
  auto_ids: true
  syntax_highlighter: rouge
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


As explained in the [concepts section](https://eslam-gomaa.github.io/Flexible-Network/concepts/#3-error-detection), the error detection is handeled differently based on the vendor
* The default vendor is Cisco

This example will show you how to specify different vendor, _the vendor must supported._ (to be documented)

Script used in this example can be found in this directory: [Code Samples](https://github.com/eslam-gomaa/Flexible-Network/tree/develop/docs/code_samples)


---

<link rel="stylesheet" href="{{ site.baseurl }}/css/custom.css">

<script src="https://gist.github.com/eslam-gomaa/3ae3239ec85559dd3b7254f548c99ca1.js"></script>

---

### Run the script

```bash
python3.6 sample-4.py -n task-4 --config ~/flexible_network.cfg  --inventory user/hosts
```

