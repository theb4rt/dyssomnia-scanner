from flask import request
from abc import ABC, abstractmethod
from functools import wraps


class Middleware(ABC):
    @abstractmethod
    def handler(self, request):
        pass


def middleware(middlewareCls, *dargs, **dkwargs):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            mid = middlewareCls(*dargs, **dkwargs)
            mid.handler(request)
            return f(*args, **kwargs)
        return wrapper
    return decorator
