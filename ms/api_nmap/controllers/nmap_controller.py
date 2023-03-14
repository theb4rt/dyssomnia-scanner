from flask_restful import Api, Resource
from flask import request

from ms.api_nmap.service.nmap_launcher_service import NmapLauncherService


class ScanByPortsController(Resource):
    def __init__(self, nmap_launcher_service: NmapLauncherService):
        self.nmap_launcher_service = nmap_launcher_service

    def post(self):
        request_data = request.get_json(silent=True)

        status, message, data, code = self.nmap_launcher_service.scan_by_port_list(data=request_data).values()

        if status:
            result = {'data': data, 'message': message}, code
        else:
            result = {'message': message, 'data': data}, code

        return result
