"""
Created on 4/2/22
@author: b4rt
@mail: root.b4rt@gmail.com
"""

from flask_marshmallow import Schema
from marshmallow.fields import Nested, Str, Number,Dict,List


class NmapProfileSchema(Schema):
    class Meta:
        fields = ["id","profile_name", "ip"]

    id = Number()
    profile_name = Str()
    ip = Str()




