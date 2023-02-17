from flask import request
from flask_restful import Api, Resource

from ..services.user_service import UserService


class RegisterController(Resource):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def post(self):
        user_data = request.get_json(silent=True)

        status, message, data, code = self.user_service.register_user(user_data).values()

        if status:
            result = {'data': data}, code
        else:
            result = {'message': message, 'data': data}, code

        return result
