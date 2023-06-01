from flask_marshmallow import Schema

from ms.helpers import is_valid_data
from ms.helpers.response import response_ok, response_error
from typing import Dict, Any, Tuple, Union

from ms.utils.logger import error_logger, info_logger


class BadMethodCallException(Exception):
    def __init__(self, message="", *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)


class BaseService:
    def __init__(self) -> None:
        self._response_error = response_error
        self._response_ok = response_ok
        self._error_logger = error_logger
        self._info_logger = info_logger
        self._is_valid_data = is_valid_data

    @classmethod
    def action(cls, method: str, *args, **kwargs) -> Any:
        try:
            action = getattr(cls(), method)
            return action(*args, **kwargs)
        except AttributeError:
            raise BadMethodCallException(f"Method {cls.__name__}.{method} does not exist.")

    def response_ok(self, status: bool = True, message: str = '', data: Any = None, code: int = 200) -> Dict[str, Any]:
        if data is None:
            data = {}

        return response_ok(status, message, data, code)

    def response_error(self, status: bool = False, message: str = '', data: Any = None, code: int = 500) -> Dict[str, Any]:
        if data is None:
            data = {}
        return response_error(status, message, data, code)
