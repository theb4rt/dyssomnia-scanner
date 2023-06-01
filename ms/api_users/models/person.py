import uuid

from sqlalchemy.dialects.postgresql import UUID

from ms.db import db


class Person(db.Model):
    __tablename__ = 'person'
    _fillable = (
        'name',
        'profile_image',
        'music',
        'user_id',
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), nullable=False, default='anonymous')
    profile_image = db.Column(db.String(120), nullable=True)
    music = db.Column(db.String(120), nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<Person {}>'.format(self.name)

    def __init__(self, data=None):
        if data is not None:
            self.set_attributes(data)
