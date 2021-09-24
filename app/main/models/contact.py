from datetime import datetime
from app import db


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now)
    is_individual = db.Column(db.Boolean, default=False)
    is_company = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=False)
    company = db.relationship('Company', backref='contact_company', uselist=False)
