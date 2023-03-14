# -*- coding: utf-8 -*-
"""
Created on 2/21/22
@author: b4rt
@mail: root.b4rt@gmail.com
"""
from urllib import request
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from ms import app
from ms.api_nmap.controllers import ScanByPortsController, BasicScanController, AllPortsScanController, \
    PortsScriptsController

from ms.api_nmap.service.nmap_launcher_service import NmapLauncherService

api_bp = Blueprint('nmap_api', __name__)
api = Api(api_bp)

api.add_resource(ScanByPortsController, "/scan-by-ports", resource_class_args=[NmapLauncherService()])
api.add_resource(BasicScanController, "/basic-scan", resource_class_args=[NmapLauncherService()])
api.add_resource(AllPortsScanController, "/all-ports-scan", resource_class_args=[NmapLauncherService()])
api.add_resource(PortsScriptsController, "/ports-scripts-scan", resource_class_args=[NmapLauncherService()])
