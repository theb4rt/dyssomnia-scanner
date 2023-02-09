"""
Created on 4/1/22
@author: b4rt
@mail: root.b4rt@gmail.com
"""
from flask_sqlalchemy import Model as BaseModel


class Model(BaseModel):
    _fillable = list()

    def setAttrs(self, data: dict) -> None:
        for key, value in data.items():
            if key in self._fillable:
                setattr(self, key, value)
    def update(self, data: dict) -> None:
        self.setAttrs(data)