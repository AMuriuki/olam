from app.main.models.partner import Partner
from app import db


class Organization(Partner):
    id = db.Column(db.Integer, db.ForeignKey('contact.id'), primary_key=True)
