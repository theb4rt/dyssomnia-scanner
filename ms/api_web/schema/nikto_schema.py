from flask_marshmallow import Marshmallow
from marshmallow import fields

from ms import app

ma = Marshmallow(app)


class NiktoScanDetailsDollarSchema(ma.Schema):
    targetip = fields.Str(required=True)
    targethostname = fields.Str(required=True)
    targetport = fields.Str(required=True)
    targetbanner = fields.Str(required=True)
    starttime = fields.String(required=True)
    sitename = fields.URL(required=True)
    siteip = fields.URL(required=True)
    hostheader = fields.Str(required=True)
    errors = fields.Int(required=True)
    checks = fields.Int(required=True)


class NiktoScanDetailsSchema(ma.Schema):
    dollar = fields.Nested(NiktoScanDetailsDollarSchema, required=True, data_key="$")  # use data_key to allow "$" in the JSON
    item = fields.List(fields.Dict(), required=True)
    ssl = fields.List(fields.Dict(), required=True)
    statistics = fields.List(fields.Dict(), required=True)


class NiktoDollarSchema(ma.Schema):
    hoststest = fields.Int(required=True)
    options = fields.Str(required=True)
    version = fields.Str(required=True)
    scanstart = fields.String(required=True)
    scanend = fields.String(required=True)
    scanelapsed = fields.Str(required=True)
    nxmlversion = fields.Str(required=True)


class NiktoScanSchema(ma.Schema):
    dollar = fields.Nested(NiktoDollarSchema, required=True, data_key="$")  # use data_key to allow "$" in the JSON
    scandetails = fields.Nested(NiktoScanDetailsSchema, many=True)


class NiktoSchema(ma.Schema):
    host = fields.URL(required=True, allow_none=False)
    niktoscan = fields.Nested(NiktoScanSchema, required=True)
