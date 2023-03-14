import re

from flask_marshmallow import Marshmallow
from marshmallow import fields, validates
from marshmallow.validate import Length

from ms import app

ma = Marshmallow(app)


class NmapScanSchema(ma.Schema):
    ip = fields.IPv4(required=True, allow_none=False)
    port_list = fields.List(fields.Int(), required=False, allow_none=False)
