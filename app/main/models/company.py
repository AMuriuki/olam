from sqlalchemy.orm import backref
from app import db
from datetime import datetime


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)  # company name
    domain_name = db.Column(db.String(120), index=True, unique=True)
    report_header = db.Column(db.Text())
    report_footer = db.Column(db.Text())
    logo = db.Column(db.String(200))
    registered_on = db.Column(db.DateTime, default=datetime.now)
    database_id = db.Column(db.Integer, db.ForeignKey('database.id'))
    street = db.Column(db.String(100))
    street2 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    county = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_address = db.Column(db.String(100))
    postal_code = db.Column(db.String(100))
    email = db.Column(db.String(120), index=True, unique=True)
    mobile_no = db.Column(db.String(120), index=True)
    website = db.Column(db.String(120), index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('company_category.id'))
    partners = db.relationship('Partner', backref='company', lazy='dynamic')
    users = db.relationship('Users', backref='company', lazy='dynamic')
    leads = db.relationship('Lead', backref='company_owning', lazy='dynamic')


class CompanyCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
