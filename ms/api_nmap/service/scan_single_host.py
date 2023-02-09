# -*- coding: utf-8 -*-
"""
Created on 2/27/22
@author: b4rt
@mail: root.b4rt@gmail.com
"""


class ScanSingleHost:
    def __init__(self, ip, port=None, timeout=None, threads=None, verbose=None, output=None, output_file=None,
                 output_json=None, command=None):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.threads = threads
        self.verbose = verbose
        self.output = output
        self.output_file = output_file
        self.output_json = output_json
        self.command = command

    def initial_scan(self):
        import subprocess
        self.output = subprocess.check_output(self.nmap_command, shell=True)



