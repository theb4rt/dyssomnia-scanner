from flask import abort
from sqlalchemy import or_
from .middleware import Middleware
from ms import app as ms_app
from ..api_users.repositories import UserRepository


class RoleMiddleware(Middleware):
    def __init__(self, roles):
        self.roles = roles
        self.user_id = None

    def handler(self, request):
        self.user_id = request.auth.get("sub")
        print("RoleMiddleware: user_id", self.user_id)

        validate_admin = self.validate_is_admin()

        for r in validate_admin:
            print("RoleMiddleware: RRRRRRRR valid " + r)

            if r in self.roles:
                return True
        abort(403)

    def validate_is_admin(self, user_id=None):
        if user_id is None:
            user_id = self.user_id
        users_repo = UserRepository()
        is_admin = users_repo.check_admin(id=user_id)
        if is_admin:
            return ['admin']
        return ['client']
