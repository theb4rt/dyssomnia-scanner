import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import TEXT

from ms.db import db


class NiktoScanResults(db.Model):
    __tablename__ = 'nikto'
    _fillable = (
        'scan_date',
        'target_url',
        'ip_address',
        'server_banner',
        'potentially_sensitive_files',
        'server_misconfigurations',
        'potential_vulnerabilities',
        'nikto_scan_id',
        'scan_duration',
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    target_url = db.Column(db.String(255), nullable=False, default='default_url')
    ip_address = db.Column(db.String(45), nullable=False, default='0.0.0.0')
    server_banner = db.Column(db.String(255), default='default_banner')
    potentially_sensitive_files = db.Column(TEXT, default='')
    server_misconfigurations = db.Column(TEXT, default='')
    potential_vulnerabilities = db.Column(TEXT, default='')
    nikto_scan_id = db.Column(db.String(255), default='default_id')
    scan_duration = db.Column(db.String(255), default='default_duration')

    def __init__(self, data=None):
        if data is not None:
            self.set_attributes(data)

    def __repr__(self):
        return f"<NiktoScanResults(id={self.id}, target_url={self.target_url}, ip_address={self.ip_address})>"
