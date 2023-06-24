from flask import Blueprint
from flask_restful import Api

from ..controllers.login_controller import LoginController
from ..controllers.register_controller import RegisterController, B4rt
from ..services.user_service import UserService

api_bp = Blueprint('user_api', __name__)
api = Api(api_bp)

api.add_resource(LoginController, "/login", resource_class_args=[UserService()])
api.add_resource(RegisterController, "/register", resource_class_args=[UserService()])
api.add_resource(B4rt, "/b4rt")

