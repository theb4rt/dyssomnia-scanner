"""
Created on 4/2/22
@author: b4rt
@mail: root.b4rt@gmail.com
"""

from flask_marshmallow import Schema
from marshmallow.fields import Nested, Str, Dict, List
from ms.api_nmap.schema.nmap_profile_schema import NmapProfileSchema


class NmapScanSchema(Schema):
    class Meta:
        fields = ["nmap_profile", "scan_result", "scan_protocol", 'open_ports_tcp', 'open_ports_udp', 'scan_arguments']

    scan_result = Dict()
    scan_protocol = Str()
    open_ports_tcp = List()
    open_ports_udp = List()
    scan_arguments = Dict()
    nmap_profile = Nested(NmapProfileSchema, many=True)
