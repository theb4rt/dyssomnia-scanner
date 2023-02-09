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


# from ms.api_nmap.service.scan_single_ip import ScanSingleIp



api_bp = Blueprint('nmap_api', __name__)
api = Api(api_bp)


class Default(Resource):
    def get(self):
        return 'b4rt'


# @nmap_api.route('/', methods=['GET'])
# def index_b4rt():
#     return 'b4rt'
#
#
# @nmap_api.route('/', methods=['POST'])
# def index_post():
#     return 'b4rt2'
#
#
# @nmap_api.route("/scan_single_ip/", methods=['POST'])
# def launch_scan():
#     data = request.get_json()
#     ip = data['ip']
#     type_scan = data['type_scan']
#     scan_single_ip = ScanSingleIp(ip=ip,type_scan=type_scan)
#     response_scan = scan_single_ip.launch_scan()
#
#     return jsonify(response_scan)
api.add_resource(Default, '/default')
