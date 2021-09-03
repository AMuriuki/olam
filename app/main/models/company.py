from app import db
from datetime import datetime


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    domain_name = db.Column(db.String(120), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    registered_on = db.Column(db.DateTime, default=datetime.now)
    database_id = db.Column(db.Integer, db.ForeignKey('database.id'))
