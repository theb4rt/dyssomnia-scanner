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
from ms.api_nmap.service.utils.logger import error_logger, info_logger


class ScanSingleIp:
    def __init__(self, ip, type_scan, ports=None, timeout=None, threads=None, verbose=None, output=None,
                 output_file=None, output_json=None, command=None, output_file_xml=None):
        self.nmap_command = None
        self.ip = ip
        self.ports = ports
        self.timeout = timeout
        self.timing = 'T3'
        self.threads = threads
        self.verbose = verbose
        self.output_name = "output_files/scan_" + self.ip
        self.output_xml = output_file_xml
        self.output_file = output_file
        self.output_json = output_json
        self.type_scan = type_scan

        self.command = command

    def basic_scan(self):
        self.nmap_command = "nmap -sS -{0} -Pn -oA {1} {2}".format(self.timing, self.output_name, self.ip)

    def scan_all_ports(self):
        self.nmap_command = "nmap -sS -{0} -Pn -p 1-65535 -oA {1} {2}".format(self.timing, self.output_name, self.ip)

    def deep_scan_by_ports(self):
        self.nmap_command = "nmap -sS -{0} -Pn -sV -sC -O -p {1} -oA {2} {3}".format(self.timing, self.ports,
                                                                                     self.output_name,
                                                                                     self.ip)
        launch = sp.Popen(self.nmap_command, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
        launch.wait()
        with open(self.output_name + '.xml', 'r') as file:
            xml = file.read()
            xml = xmltodict.parse(xml)
        print(json.dumps(xml))

    def get_open_ports(self):
        output = sp.Popen(self.nmap_command, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
        output.wait()
        with open(self.output_name + '.xml', 'r') as file:
            self.output_xml = file.read()

        self.upload_files_s3()
        self.output_json = xmltodict.parse(self.output_xml)
        info_logger.info(json.loads(json.dumps(self.output_json))['nmaprun']['host']['ports'])
        return self.return_open_ports()

    def parse_json_output(self):
        host = self.output_json['nmaprun']['host']
        ports = None
        try:
            ports = host['ports']['port']
            info_logger.info(json.loads(json.dumps(ports)))
        except KeyError:
            error_logger.error("No ports found for host: {0}".format(self.ip))

        return ports

    def return_open_ports(self):
        ports = self.parse_json_output()
        open_ports = []

        if ports:
            if type(ports) is list:
                open_ports = [port['@portid'] for port in ports if port['state']['@state'] == 'open']
            else:
                open_ports = [ports['@portid']]

        return open_ports

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
