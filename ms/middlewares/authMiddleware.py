from flask import abort
from ms.helpers.jwt_config import JwtHelper
from .middleware import Middleware

from ..api_users.repositories import UserRepository
from ..utils import error_logger


class AuthMiddleware(Middleware):
    def __init__(self):
        self.roles = None

    def handler(self, request):
        jwtHelper = JwtHelper()
        users_repo = UserRepository()

        auth = request.headers.get('Authorization')

        if not auth:
            error_logger.error("no auth")
            abort(403)

        valid = jwtHelper.check(auth)

        if not valid:
            error_logger.error("AuthMiddleware: not valid")
            abort(403)

        payload = jwtHelper.decode(auth)
        user_id = payload['sub']
        user = users_repo.find_user(id=user_id)

        if not user:
            error_logger.error("User not found: not valid")
            abort(403)

        setattr(request, 'auth', payload)
        return True
