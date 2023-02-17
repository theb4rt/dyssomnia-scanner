def response_ok(status=True, message='', data=None, code=200):
    if data is None:
        data = {}

    return {
        'status': status,
        'message': message,
        'data': data,
        'code': code
    }


def response_error(status=False, message='', data=None, code=500):
    if data is None:
        data = {}
    return {
        'status': status,
        'message': message,
        'data': data,
        'code': code
    }
