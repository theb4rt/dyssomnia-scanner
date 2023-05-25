import re

from flask_marshmallow import Marshmallow
from marshmallow import fields, validates
from marshmallow.validate import Length

from ms import app

ma = Marshmallow(app)


class NiktoSchema(ma.Schema):
    host = fields.URL(required=True, allow_none=False)
    extra_options = fields.String(required=False, allow_none=True)
