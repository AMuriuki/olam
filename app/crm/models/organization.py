from app.main.models.contact import Contact
from app import db


class Organization(Contact):
    id = db.Column(db.Integer, db.ForeignKey('contact.id'), primary_key=True)
