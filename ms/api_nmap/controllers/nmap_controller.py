from flask_restful import Api, Resource
from flask import request

from ms.api_nmap.service.nmap_launcher_service import NmapLauncherService
from ms.middlewares import AuthMiddleware, middleware, RoleMiddleware


class ScanByPortsController(Resource):
    def __init__(self, nmap_launcher_service: NmapLauncherService):
        self.nmap_launcher_service = nmap_launcher_service

    @middleware(AuthMiddleware)
    @middleware(RoleMiddleware, roles=('admin', 'client'))
    def post(self):
        request_data = request.get_json(silent=True)

        status, message, data, code = self.nmap_launcher_service.scan_by_port_list(data=request_data).values()

        if status:
            result = {'data': data, 'message': message}, code
        else:
            result = {'message': message, 'data': data}, code

        return result


class BasicScanController(Resource):
    def __init__(self, nmap_launcher_service: NmapLauncherService):
        self.nmap_launcher_service = nmap_launcher_service

    @middleware(AuthMiddleware)
    @middleware(RoleMiddleware, roles=('admin', 'client'))
    def post(self):
        request_data = request.get_json(silent=True)
        status, message, data, code = self.nmap_launcher_service.basic_scan(data=request_data).values()

        if status:
            result = {'data': data, 'message': message}, code
        else:
            result = {'message': message, 'data': data}, code

        return result


class AllPortsScanController(Resource):
    def __init__(self, nmap_launcher_service: NmapLauncherService):
        self.nmap_launcher_service = nmap_launcher_service

    @middleware(AuthMiddleware)
    @middleware(RoleMiddleware, roles=('admin'))
    def post(self):
        request_data = request.get_json(silent=True)
        status, message, data, code = self.nmap_launcher_service.all_ports_scan(data=request_data).values()

        if status:
            result = {'data': data, 'message': message}, code
        else:
            result = {'message': message, 'data': data}, code
        return result


class PortsScriptsController(Resource):
    def __init__(self, nmap_launcher_service: NmapLauncherService):
        self.nmap_launcher_service = nmap_launcher_service

    @middleware(AuthMiddleware)
    @middleware(RoleMiddleware, roles=('admin', 'client'))
    def post(self):
        request_data = request.get_json(silent=True)
        status, message, data, code = self.nmap_launcher_service.scan_ports_and_scripts(data=request_data).values()

        if status:
            result = {'data': data, 'message': message}, code
        else:
            result = {'message': message, 'data': data}, code

        return result
