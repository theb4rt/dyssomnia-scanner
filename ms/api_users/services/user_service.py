import os
import sys

from sqlalchemy.exc import SQLAlchemyError

from secrets import compare_digest
import bcrypt

from ..repositories import UserRepository
from ..schema.login_schema import LoginSchema, RegisterSchema
from ms.helpers.schema_validator import is_valid
from ms.services.service import BaseService
from ..serializers import RegisterSerializer, LoginSerializer
from ...helpers.jwt_config import JwtHelper
from typing import Tuple, Dict, Any


class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.user_repo = UserRepository()

    def _is_valid_user_data(self, user_data: dict) -> Tuple[bool, Dict[str, Any]]:
        if user_data is None:
            return False, {"error": "Invalid Json"}

        login_schema = LoginSchema()
        return is_valid(login_schema, user_data)

    def _is_valid_user_register(self, user_data: dict) -> Tuple[bool, Dict[str, Any]]:
        if user_data is None:
            return False, {"error": "Invalid Json"}

        register_schema = RegisterSchema()
        return is_valid(register_schema, user_data)

    def register_user(self, user_data: dict) -> Dict[str, Any]:
        status, result = self._is_valid_user_data(user_data)

        hashed_password = self._hash_password(user_data["password"])
        result['password'] = hashed_password
        if not status:
            return self.response_error(data=result, code=400)

        try:

            user = self.user_repo.add(data=result)

            if user is None:
                return self.response_error(message="Username is taken", code=400)
            serializer = RegisterSerializer(user)
            return self.response_ok(data=serializer.get_data(), message="User successfully registered", code=201)
        except SQLAlchemyError as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return self.response_error(message="Please contact an administrator")

    def login_user(self, user_data: dict) -> Dict[str, Any]:
        status, result = self._is_valid_user_register(user_data)

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
