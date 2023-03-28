"""repwires.py - This module contains the class that calculates the data for the wires report."""
from typing import Any, Dict, List

from netutils.interface import abbreviated_interface_name

# Outlook: Excel Export of the report data
#     Excel:     https://xlsxwriter.readthedocs.io/example_django_simple.html
#     In Memory: https://xlsxwriter.readthedocs.io/example_http_server.html?highlight=in%20memory#example-simple-http-server
#


class CalculateWiresReportData:
    """This class calculates the data for the wires report."""

    wired_ports: List[Dict[str, Any]] = []
    report_data: Dict[str, Any] = {}
    header_fields = {}

    def __init__(self, device):
        """Initialize the class.

        Args:
            device (Device): The device to calculate the report data for.
        """
        self.wired_ports = []
        self.header_fields = []
        self.report_data = {}
        self.device = device
        self.get_wired_ports(self.device)
        self.get_wire_report()

    def get_wired_ports(self, device):
        """Get all ports of a device that are cabled and update the self.cabled_ports list.

        Multiple Calls will add data to the list.

        Args:
            device (Device): Device object
        """
        devices = [device]
        # Check if device is part of a virtual chassis
        if device.virtual_chassis and device.virtual_chassis.members.count() > 1:
            # Get all devices of the virtual chassis
            devices = device.virtual_chassis.members.all()

        for curr_device in devices:
            self.device = curr_device
            for ports in curr_device.interfaces, curr_device.frontports, curr_device.rearports:
                if ports is not None:
                    for port in ports.all():
                        port_device = port.device
                        if port.cable is not None:
                            if port.cable.termination_a.device.id == port_device.id:
                                device_termination = port.cable.termination_a
                                device_type = port.cable.termination_a_type.model
                                # termination_b == peer
                                peer_device = port.cable.termination_b.device
                                peer_type = port.cable.termination_b_type.model
                                peer_termination = port.cable.termination_b
                            elif port.cable.termination_b.device.id == port_device.id:
                                device_termination = port.cable.termination_b
                                device_type = port.cable.termination_b_type.model
                                # termination_a == peer
                                peer_device = port.cable.termination_a.device
                                peer_type = port.cable.termination_a_type.model
                                peer_termination = port.cable.termination_a
                            else:
                                continue
                            # Add port to list
                            info = {
                                "cable": port.cable,
                                "device_port": port,
                                "device_termination": device_termination,
                                "device_type": device_type,
                                "device": port.device,
                                "peer_device": peer_device,
                                "peer_type": peer_type,
                                "peer_termination": peer_termination,
                            }
                            self.wired_ports.append(info)

    def get_wire_report(self):
        """Calculate the report data."""
        if not self.wired_ports:
            return

        if not self.report_data:
            self.header_fields = {
                "device_model": "Device-Model",
                "device_position": "Device-Position",
                "device_rack": "Device-Rack",
                "device_rack_facility_id": "Device-Facility-Id",
                "device_name": "Device",
                "device_port_name": "Device-Port/Interface",
                "device_port_type": "Port-Type",
                "cable_type": "Cable",
                "cable_label": "Cable-Label",
                "cable_status": "Cable-Status",
                "peer_port_type": "Conn-Port-Type",
                "peer_port_name": "Conn-Port/Interface",
                "peer_device_name": "Conn-to",
                "peer_model": "Conn-Model",
                "peer_position": "Conn-Position",
                "peer_rack": "Conn-Rack",
                "peer_rack_facility_id": "Conn-Facility-Id",
                "wired_port": "Wired-port",
            }

        for con in self.wired_ports:
            # initialize report_data for new device
            device_name = con["device_termination"].device.name
            if con["device_termination"].device.name not in self.report_data:
                self.report_data.update({device_name: []})

            try:
                device_model = con["device_port"].device.device_type.model  # 'LWL-24xLC-FD'
            except Exception:
                device_model = "---"
            try:
                device_position = f"U{con['device_port'].device.position}"  # U40
            except Exception:
                device_position = "---"
            try:
                device_rack = con["device_port"].device.rack.name  # "Rack-DC0-1"
            except Exception:
                device_rack = "---"
            try:
                device_rack_facility_id = con["device_port"].device.rack.facility_id  # "RDC0-1, Server Room 1st Floor"
            except Exception:
                device_rack_facility_id = "---"

            try:
                peer_model = con["peer_termination"].device.device_type.model  # 'LWL-24xLC-FD'
            except Exception:
                peer_model = "---"
            try:
                peer_position = f"U{con['peer_termination'].device.position}"  # U40
            except Exception:
                peer_position = "---"
            try:
                peer_rack = con["peer_termination"].device.rack.name  # "Rack-DC0-1"
            except Exception:
                peer_rack = "---"
            try:
                peer_rack_facility_id = con[
                    "peer_termination"
                ].device.rack.facility_id  # "RDC0-1, Server Room 1st Floor"
            except Exception:
                peer_rack_facility_id = "---"

            data = {
                "device_model": device_model,
                "device_position": device_position,
                "device_rack": device_rack,
                "device_rack_facility_id": device_rack_facility_id,
                "device_name": con["device_termination"].device.name,
                "device_port_name": abbreviated_interface_name(con["device_port"].name),
                "device_port_type": con["device_port"].type,
                "cable_type": con["cable"].type,
                "cable_label": con["cable"].label,
                "cable_status": con["cable"].status.name,
                "peer_port_type": con["peer_termination"].type,
                "peer_port_name": abbreviated_interface_name(con["peer_termination"].name),
                # # customize peer_device_name (truncate site name)
                # "peer_device_name": con["peer_termination"].device.name.split("__@")[0],
                "peer_device_name": con["peer_termination"].device.name,
                "peer_model": peer_model,
                "peer_position": peer_position,  # Conn-Position
                "peer_rack": peer_rack,  # Conn-Rack
                "peer_rack_facility_id": peer_rack_facility_id,  # Conn-Facility-Id
                "wired_port": con,  # Allow access to all data in jinja template
            }
            self.report_data[device_name].append(data)
