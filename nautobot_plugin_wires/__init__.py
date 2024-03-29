"""Nautobot-Plugin-Wires."""
try:
    from importlib import metadata
except ImportError:
    # Python version < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import PluginConfig


class WiresPluginConfig(PluginConfig):
    """Plugin configuration class."""

    name = "nautobot_plugin_wires"
    verbose_name = "Nautobot Plugin Wires"
    author = "Josef Fuchs"
    author_email = "josef.fuchs@j-fuchs.at"
    version = __version__
    description = "Nautobot Plugin to add tab [Wires] to device detail page"
    base_url = "wires"
    min_version = "1.4.0"
    # max_version = "1.9.99"
    middleware = []
    installed_apps = ["nautobot.extras.tests.example_plugin_dependency"]


config = WiresPluginConfig  # pylint: disable=C0103
