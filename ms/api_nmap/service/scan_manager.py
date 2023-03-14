# -*- coding: utf-8 -*-
"""
Created on 2/27/22
@author: b4rt
@mail: root.b4rt@gmail.com
"""
import os
import subprocess as sp

import xmltodict
import json

from ms import app
from ms.api_nmap.service.utils.logger import error_logger, info_logger


class ScanManager:
    def __init__(self, ip='127.0.0.1', type_scan='sT', ports=None, timeout=None, threads=None, verbose=None,
                 output=None,
                 output_file=None, output_json=None, command=None, output_file_xml=None):
        self.nmap_command = None
        self.ip = ip
        self.ports = ports
        self.timeout = timeout
        self.timing = 'T3'
        self.threads = threads
        self.verbose = verbose
        self.output_name = app.config.get('APP_ROOT') + "/ms/api_nmap/output_files/scan_" + str(self.ip) + "_file"
        self.output_xml = output_file_xml
        self.output_file = output_file
        self.output_json = output_json
        self.type_scan = type_scan
        self.open_ports = []
        self.open_ports_services = {}
        self.command = command

    def basic_scan(self):

        self.nmap_command = ["nmap", self.ip, "-Pn", self.type_scan, self.timing, "-oA",
                             self.output_name]
        self.launch_nmap()
        return self.open_ports_services

    def scan_all_ports(self):

        self.nmap_command = ["nmap", self.ip, "-Pn", self.type_scan, self.timing, "-p", "1-65535", "-oA",
                             self.output_name]
        self.launch_nmap()
        return self.open_ports_services

    def scan_scripts_ports(self):
        self.nmap_command = ["nmap", self.ip, "-Pn", self.type_scan, "-sC", self.timing, "-p", self.ports, "-oA",
                             self.output_name]
        self.launch_nmap()
        return self.open_ports_services

    def scan_by_ports(self):

        self.nmap_command = ["nmap", self.ip, "-Pn", self.type_scan, self.timing, "-p", self.ports, "-oA",
                             self.output_name]

        self.launch_nmap()
        return self.open_ports_services

    def launch_nmap(self):

        output = sp.Popen(self.nmap_command, shell=False, stdout=sp.PIPE, stderr=sp.STDOUT)
        output.wait()
        with open(self.output_name + '.xml', 'r') as file:
            self.output_xml = file.read()
            self.output_json = xmltodict.parse(self.output_xml)
        self.upload_files_s3()
        info_logger.info(json.loads(json.dumps(self.output_json))['nmaprun']['host']['ports'])
        self.get_open_port_services()

    def parse_json_output(self):
        host = self.output_json['nmaprun']['host']
        ports = None
        try:
            ports = host['ports']['port']

            info_logger.info(json.loads(json.dumps(ports)))
        except KeyError:
            error_logger.error("No ports found for host: {0}".format(self.ip))
        return ports

    def get_open_port_services(self):
        ports = self.parse_json_output()
        open_ports_services = {}

        if ports:
            if type(ports) is list:
                for port in ports:
                    if port['state']['@state'] == 'open':
                        open_ports_services[port['@portid']] = port.get('service', {}).get('@name', "unknown")
            else:
                open_port = ports['@portid']
                open_service = ports.get('service', {}).get('@name', "unknown")
                open_ports_services[open_port] = open_service

        self.open_ports_services = open_ports_services

    def upload_files_s3(self):
        try:
            os.remove(self.output_name + '.xml')
            os.remove(self.output_name + '.nmap')
            os.remove(self.output_name + '.gnmap')
        except OSError as e:
            error_logger.error(e)

    def launch_scan(self):
        # ports_initial_scan = self.initial_scan()
        # all_open_ports = self.scan_all_ports()
        self.scan_all_ports()
        open_ports = self.get_open_ports()
        self.ports = open_ports
        deep_scan_by_ports = self.deep_scan_by_ports()

        return open_ports
