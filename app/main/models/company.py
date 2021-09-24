from app import db
from datetime import datetime


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    domain_name = db.Column(db.String(120), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    registered_on = db.Column(db.DateTime, default=datetime.now)
    database_id = db.Column(db.Integer, db.ForeignKey('database.id'))
    street = db.Column(db.String(100))
    street2 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    county = db.Column(db.String(100))
    county = db.Column(db.String(100))
    postal_address = db.Column(db.String(100))
    postal_code = db.Column(db.String(100))
    email = db.Column(db.String(120), index=True, unique=True)
    mobile_no = db.Column(db.String(120), index=True)
    website = db.Column(db.String(120), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('company_category.id'))


class CompanyCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
