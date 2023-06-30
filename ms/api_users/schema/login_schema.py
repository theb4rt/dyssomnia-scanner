from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow.validate import Length

from ms import app

ma = Marshmallow(app)


class LoginSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True, allow_none=False, validate=Length(min=1, max=100))
    email = fields.Email(required=False, allow_none=False)
    password = fields.String(required=True, allow_none=False, validate=Length(min=1, max=100))


class RegisterSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True, allow_none=False, validate=Length(min=1, max=100))
    email = fields.Email(required=False, allow_none=False)
    password = fields.String(required=True, allow_none=False, validate=Length(min=1, max=100))
    name = fields.String(required=False, allow_none=False, validate=Length(min=1, max=100))
