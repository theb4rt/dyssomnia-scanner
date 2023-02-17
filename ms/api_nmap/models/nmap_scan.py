"""
Created on 4/1/22
@author: b4rt
@mail: root.b4rt@gmail.com
"""
from ms.db import db


class NmapScan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nmap_profile = db.Column(db.Integer, db.ForeignKey('nmap_profile.id'))
    scan_result = db.Column(db.JSON, nullable=True)
    scan_protocol = db.Column(db.String(4), nullable=True)
    open_ports_tcp = db.Column(db.JSON, nullable=True)
    open_ports_udp = db.Column(db.JSON, nullable=True)
    scan_arguments = db.Column(db.JSON, nullable=True)

    def __init__(self, nmap_profile, scan_result, scan_protocol, open_ports_tcp, open_ports_udp, scan_arguments):
        self.nmap_profile = nmap_profile
        self.scan_result = scan_result
        self.scan_protocol = scan_protocol
        self.open_ports_tcp = open_ports_tcp
        self.open_ports_udp = open_ports_udp
        self.scan_arguments = scan_arguments

