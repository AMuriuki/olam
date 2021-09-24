from datetime import datetime
from app import db


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=False)
