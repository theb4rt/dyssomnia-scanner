from flask import Blueprint
from flask_restful import Api

from ..controllers.nikto_controller import NiktoController
from ..services.nikto_service import NiktoService

api_bp = Blueprint('nikto_api', __name__)
api = Api(api_bp)

api.add_resource(NiktoController, "/nikto", resource_class_args=[NiktoService()])
