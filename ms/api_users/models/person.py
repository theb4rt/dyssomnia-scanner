import uuid

from sqlalchemy.dialects.postgresql import UUID

from ms.db import db


class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), nullable=False)
    profile_image = db.Column(db.String(120), nullable=False)
    music = db.Column(db.String(120), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('persons', lazy=True))

    def __repr__(self):
        return '<Person {}>'.format(self.name)

    def __init__(self, data=None):
        if data is not None:
            self.set_attributes(data)
