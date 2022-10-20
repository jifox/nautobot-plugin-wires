# views.py
from django.shortcuts import render

from nautobot.core.views import generic
from nautobot.dcim.models import Device

from .repwires import CalculateWiresReportData


class DeviceDetailWiresTab(generic.ObjectView):
    """
    This view's template extends the device detail template,
    making it suitable to show as a tab on the device detail page.

    Views that are intended to be for an object detail tab's content rendering must
    always inherit from nautobot.core.views.generic.ObjectView.
    """

    queryset = Device.objects.all()
    template_name = "nautobot_plugin_wires/tab_device_detail_wires.html"

    def get(self, request, pk):
        """
        This method is called when a GET request is made to the view.

        The request and pk are passed to the view from the URL definition.
        """
        device = Device.objects.get(id=pk)
        report = CalculateWiresReportData(device)
        wired_ports = report.wired_ports
        header = report.header_fields
        report_data = report.report_data

        return render(
            request=self.request,
            template_name=self.template_name,
            context={
                "object": device,
                "wired_ports": wired_ports,
                "header": header,
                "report_data": report_data,
            },
        )
