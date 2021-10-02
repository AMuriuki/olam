from app.main.models.partner import Partner
from app import db


class Organization(Partner):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, db.ForeignKey('partner.id'), primary_key=True)
