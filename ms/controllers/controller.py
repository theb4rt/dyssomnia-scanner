class BadMethodCallException(Exception):
    def __init__(self, message="", *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)


class BaseController:
    @classmethod
    def action(cls, method, *args, **kwargs):
        try:
            action = getattr(cls(), method)
            return action(*args, *kwargs)
        except AttributeError:
            raise BadMethodCallException(
                f"Method {cls.__name__}.{method} does not exist.")
