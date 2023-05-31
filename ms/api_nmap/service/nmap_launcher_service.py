# -*- coding: utf-8 -*-
"""
Created on 2/15/23
@author: b4rt
@mail: root.b4rt@gmail.com
"""
from flask_restful import Resource

from ms.api_nmap.schema import NmapScanSchema
from ms.api_nmap.service.scan_manager import ScanManager
from ms.helpers.response import response_error, response_ok
from ms.helpers.schema_validator import is_valid
from ms.utils import error_logger


class NmapLauncherService(Resource):
    """ launch nmap to scan a single ip """

    def __init__(self):
        self.scan_manager = ScanManager()

    def scan_by_port_list(self, data) -> dict:
        status, result = self._is_valid_nmap_data(data)

        if not status:
            return response_error(data=result, code=400)

        self.scan_manager.ip = data.get('ip')
        self.scan_manager.ports = "".join(str(data.get('port_list'))[1:-1].split())

        try:
            scanned = self.scan_manager.scan_by_ports()
            return response_ok(data=scanned, code=200)

        except Exception as e:
            error_logger.error("error: %s", str(e))
            return response_error(message='There was an error', code=500)

    def basic_scan(self, data) -> dict:
        status, result = self._is_valid_nmap_data(data)
        if not status:
            return response_error(data=result, code=400)
        self.scan_manager.ip = data.get('ip')
        try:
            scanned = self.scan_manager.basic_scan()
            return response_ok(data=scanned, code=200)

        except Exception as e:
            error_logger.error("error: %s", str(e))
            return response_error(message='There was an error', code=500)

    def all_ports_scan(self, data) -> dict:
        status, result = self._is_valid_nmap_data(data)
        if not status:
            return response_error(data=result, code=400)
        self.scan_manager.ip = data.get('ip')
        try:
            scanned = self.scan_manager.scan_all_ports()
            return response_ok(data=scanned, code=200)

        except Exception as e:
            error_logger.error("error: %s", str(e))
            return response_error(message='There was an error', code=500)

    def scan_ports_and_scripts(self, data) -> dict:
        status, result = self._is_valid_nmap_data(data)
        if not status:
            return response_error(data=result, code=400)
        self.scan_manager.ip = data.get('ip')
        self.scan_manager.ports = "".join(str(data.get('port_list'))[1:-1].split())
        try:
            scanned = self.scan_manager.scan_scripts_ports()
            return response_ok(data=scanned, code=200)

        except Exception as e:
            error_logger.error("error: %s", str(e))
            return response_error(message='There was an error', code=500)

    def _is_valid_nmap_data(self, data) -> tuple:
        if data is None:
            return False, {"error": "Invalid Json"}

        nmap_schema = NmapScanSchema()
        return is_valid(nmap_schema, data)
