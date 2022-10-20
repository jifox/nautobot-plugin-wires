# <img src="./docs/img/wires.png" width="30" /> Nautobot-Plugin-Wires

A plugin to display all wired interfaces, front- and rear-ports of devices.
If a device belongs to a Virtual-Chassis than all interfaces of all members are displayed.

## Installation

This module is currently not available at PyPi. (WIP)

Use `poetry` to install the plugin from github

```bash
# Use poetry
poetry add git+https://github.com/jifox/nautobot-plugin-wires.git#main

# Install with pip
pip install git+git+https://github.com/jifox/nautobot-plugin-wires.git@main
```

## Configure plugin

```python
# nautobot_config.py

###############################
#                             #
#    WIRES-PLUGIN Settings    #
#                             #
###############################

if is_truthy(os.getenv("NAUTOBOT_WIRES_PLUGIN_ENABLED", "False")):
    if "nautobot_plugin_wires" not in PLUGINS:
        # Enable installed plugins. Add the name of each plugin to the list.
        PLUGINS.append("nautobot_plugin_wires")

    if "nautobot_plugin_wires" not in PLUGINS_CONFIG:
        # Plugins configuration settings. These settings are used by various plugins that the user may have installed.
        # Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.
        PLUGINS_CONFIG.update(
            {
                "nautobot_plugin_wires": {}
            }
        )

```

Set the environment variable `NAUTOBOT_WIRES_PLUGIN_ENABLED=True` to enable the
plugin.

## Work in Progress:

- Add Development environment
- Add Unittests
- Publish to PyPi

Outlook:

- Add ability to download Excel .xlsx

**Any help is wellcome!**
