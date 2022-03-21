from app.main.models.partner import Partner
from app import db
from sqlalchemy.dialects.postgresql import UUID


class Organization(Partner):
    __table_args__ = {'extend_existing': True}
    id = db.Column(UUID(as_uuid=True), db.ForeignKey('partner.id'), primary_key=True)
