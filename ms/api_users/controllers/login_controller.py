from flask import request
from flask_restful import Api, Resource

from ..services.user_service import UserService


class LoginController(Resource):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def post(self):
        user_data = request.get_json(silent=True)

        status, message, data, code = self.user_service.login_user(user_data).values()

        if status:
            result = {'data': data, 'message': message}, code
        else:
            result = {'message': message, 'data': data}, code

        return result
