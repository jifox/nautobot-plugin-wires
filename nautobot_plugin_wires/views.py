""" views.py: This module contains the class that renders the wires report as a tab on the device detail page."""

from django.shortcuts import get_object_or_404, render

from nautobot.dcim.models import Device
from nautobot.extras.models import Job as ChangeLoggedModel

from nautobot.apps import views


from .repwires import CalculateWiresReportData


class DeviceDetailWiresTab(views.ObjectView):
    """
    This view's template extends the device detail template,
    making it suitable to show as a tab on the device detail page.

    Views that are intended to be for an object detail tab's content rendering must
    always inherit from nautobot.core.views.generic.ObjectView.
    """

    queryset = Device.objects.all()
    template_name = "nautobot_plugin_wires/tab_device_detail_wires.html"

    def get(self, request, pk, **kwargs):
        """
        This method is called when a GET request is made to the view.

        The request and pk are passed to the view from the URL definition.
        """
        instance = get_object_or_404(Device, id=pk)

        changelog_url = None

        if isinstance(instance, ChangeLoggedModel):
            changelog_url = instance.get_changelog_url()

        report = CalculateWiresReportData(instance)
        wired_ports = report.wired_ports
        header = report.header_fields
        report_data = report.report_data

        return render(
            request=self.request,
            template_name=self.template_name,
            context={
                "object": instance,
                "wired_ports": wired_ports,
                "header": header,
                "report_data": report_data,
                "verbose_name": self.queryset.model._meta.verbose_name,
                "verbose_name_plural": self.queryset.model._meta.verbose_name_plural,
                "changelog_url": changelog_url,  # 2.0 TODO: Remove in 2.0. This information can be retrieved from the object itself now.
                **self.get_extra_context(request, instance),
            },
        )
