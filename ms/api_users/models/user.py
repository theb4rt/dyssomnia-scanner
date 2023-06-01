import uuid

from sqlalchemy.dialects.postgresql import UUID

from ms.db import db


class User(db.Model):
    __tablename__ = 'user'
    _fillable = (
        'username',
        'password',
        'email',
        'is_active',
        'is_admin'
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    person = db.relationship('Person', backref='user', uselist=False)
    nikto_scan_results = db.relationship('NiktoScanResults', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())



    def __init__(self, data=None):
        if data is not None:
            self.set_attributes(data)

    def __repr__(self):
        return f'<User {self.username} {self.email} {self.is_active} {self.is_admin}>'
