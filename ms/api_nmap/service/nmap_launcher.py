# -*- coding: utf-8 -*-
"""
Created on 2/15/22
@author: b4rt
@mail: root.b4rt@gmail.com
"""
from flask import Flask, request, jsonify
from flask_restful import Resource, Api


class NampLauncher:
    """ launch nmap to scan a single ip """

    def __init__(self, ip):
        self.ip = ip
        self.nmap_command = "nmap -sV -sC -sS -sU -p- -oX - " + self.ip
        self.nmap_output = ""

    def launch(self):
        """ launch nmap """
        import subprocess
        self.nmap_output = subprocess.check_output(self.nmap_command, shell=True)
        return self.nmap_output

    def get_output(self):
        """ get nmap output """
        return self.nmap_output

    def get_ip(self):
        """ get ip """
        return self.ip

    def get_nmap_command(self):
        """ get nmap command """
        return self.nmap_command
