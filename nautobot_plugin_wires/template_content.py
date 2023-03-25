# template_content.py
from django.urls import reverse
from nautobot.apps.ui import TemplateExtension


class DeviceExtraTabs(TemplateExtension):
    """Template extension to add extra tabs to the object detail tabs."""

    model = "dcim.device"

    def detail_tabs(self):
        """
        You may define extra tabs to render on a model's detail page by utilizing this method.
        Each tab is defined as a dict in a list of dicts.

        For each of the tabs defined:
        - The <title> key's value will become the tab link's title.
        - The <url> key's value is used to render the HTML link for the tab

        These tabs will be visible (in this instance) on the Device model's detail page as
        set by the DeviceContent.model attribute "dcim.device"

        The tabs will be ordered by their position in list.
        """
        return [
            {
                "title": "Wires",
                "url": reverse(
                    "plugins:nautobot_plugin_wires:device_detail_wires_tab",
                    kwargs={"pk": self.context["object"].pk},
                ),
            },
        ]


template_extensions = [DeviceExtraTabs]
