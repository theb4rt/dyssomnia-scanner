"""
Created on 4/1/22
@author: b4rt
@mail: root.b4rt@gmail.com
"""
from ms.db import db


class NmapProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_name = db.Column(db.String(80), nullable=True)
    ip = db.Column(db.String(64), nullable=True)

    def __init__(self, profile_name, ip):
        self.profile_name = profile_name
        self.ip = ip

    def __str__(self):
        return '<NmapProfile %r>' % self.profile_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
 