""" urls.py - URL definitions for the nautobot_plugin_wires plugin. """
from django.urls import path

from nautobot_plugin_wires import views

urlpatterns = [
    # ... previously defined urls
    path("devices/<uuid:pk>/cabling/", views.DeviceDetailWiresTab.as_view(), name="device_detail_wires_tab"),
]
