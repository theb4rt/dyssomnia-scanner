import uuid

from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import TEXT
from sqlalchemy.ext.mutable import MutableDict, MutableList

from ms.db import db


class NiktoScanResults(db.Model):
    __tablename__ = 'nikto'
    _fillable = ['target_url',
                 'ip_address',
                 'server_banner',
                 'potentially_sensitive_files',
                 'server_misconfigurations',
                 'potential_vulnerabilities',
                 'scan_duration',
                 'items',
                 'scan_full_report',
                 'scan_items_found']

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    target_url = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    server_banner = db.Column(db.String(255))
    potentially_sensitive_files = db.Column(TEXT)
    server_misconfigurations = db.Column(TEXT)
    potential_vulnerabilities = db.Column(TEXT)
    scan_duration = db.Column(db.String(255))
    items = db.Column(MutableList.as_mutable(JSONB))


    scan_full_report = db.Column(db.JSON)
    scan_items_found = db.Column(db.Integer)

    def __init__(self, data=None):
        if data is not None:
            self.set_attributes(data)

    # def __repr__(self):
    #     return f"<NiktoScanResults(id={self.id}, target_url={self.target_url}, ip_address={self.ip_address})>"
