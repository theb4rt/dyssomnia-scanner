# -*- coding: utf-8 -*-
from flask import request

from ms.helpers.response import response_error, response_ok


def request_validator(data):
    try:
        data = request.get_json()
        return response_ok(data=data)
    except Exception as e:
        print(str(e))
        return response_error(code=400, message='Invalid json')
