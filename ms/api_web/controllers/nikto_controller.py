from flask import request
from flask_restful import Api, Resource

from ..services.nikto_service import NiktoService


class NiktoController(Resource):
    def __init__(self, nikto_service: NiktoService):
        self.nikto_service = nikto_service

    def post(self):
        data = request.get_json(silent=True)
        self.nikto_service.data = data

        status, message, data, code = self.nikto_service.process_data().values()

        if status:
            result = {'data': data, 'message': message}, code
        else:
            result = {'message': message, 'data': data}, code

        return result
