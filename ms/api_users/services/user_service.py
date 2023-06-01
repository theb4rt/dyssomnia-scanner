import os
import sys
import traceback

from sqlalchemy.exc import SQLAlchemyError

from secrets import compare_digest
import bcrypt

from ..repositories import UserRepository
from ..schema.login_schema import LoginSchema, RegisterSchema
from ms.services.service import BaseService
from ..serializers import RegisterSerializer, LoginSerializer
from ...helpers.jwt_config import JwtHelper
from typing import Tuple, Dict, Any


class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.user_repo = UserRepository()

    def register_user(self, user_data: dict) -> Dict[str, Any]:
        status, result = self._is_valid_data(RegisterSchema(), user_data)
        if not status:
            return self.response_error(data=result, code=400)

        try:
            user_data = {
                'username': result['username'],
                'password': self._hash_password(result['password']),
                'email': result['email']
            }
            person_data = {
                'name': result.get('name', None)
            }

            user = self.user_repo.add_new_user(user_data=user_data, person_data=person_data)
            if not user:
                return self.response_error(message="Username is taken", code=400)

            serializer = RegisterSerializer(user)
            return self.response_ok(data=serializer.get_data(), message="User successfully registered", code=201)
        except Exception as err:
            self._error_logger.error(traceback.format_exc())
            return self.response_error(message="An unexpected error occurred", code=500)

    def login_user(self, user_data: dict) -> Dict[str, Any]:
        status, result = self._is_valid_data(LoginSchema(), user_data)

        if not status:
            return self.response_error(data=result, code=400)
        user = self.user_repo.find_user_by_username(user_data["username"])
        if user is None:
            return self.response_error(message="Invalid username or password", code=400)
        if not self._is_correct_password(user_data["password"], user.password):
            return self.response_error(message="Invalid username or password", code=400)

        user_data = self._set_payload(user)

        return self.response_ok(message='User successfully logged in', code=200, data=user_data)

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def _is_correct_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def _set_payload(self, user) -> Dict[str, Any]:
        jwt_helper = JwtHelper()

        return jwt_helper.get_tokens(
            payload={
                'user': user.username,
                'roles': ['admin' if user.is_admin else 'client'],
                'sub': str(user.id)
            }
        )
