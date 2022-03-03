from datetime import datetime
from enum import unique

from sqlalchemy.orm import backref
from app import db
from app.utils import unique_slug_generator


class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    title = db.Column(db.String(60), index=True)
    company_name = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True)
    function = db.Column(db.String(60), index=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    is_individual = db.Column(db.Boolean, default=False)
    is_company = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    title_id = db.Column(db.Integer, db.ForeignKey('partner_title.id'))
    phone_no = db.Column(db.String(120), index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    parent = db.relationship('Partner', remote_side=[id])
    website = db.Column(db.String(120), index=True)
    postal_code = db.Column(db.String(120), index=True)
    postal_address = db.Column(db.String(120), index=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    users = db.relationship('Users', backref='partner', lazy='dynamic')
    is_tenant = db.Column(db.Boolean, default=False)
    tax_id = db.Column(db.String(60), index=True)
    partnerships = db.relationship(
        'Lead', backref='opportunity', lazy='dynamic')
    teams = db.relationship('Team', backref='lead', lazy='dynamic')
    slug = db.Column(db.Text(), unique=True)
    is_archived = db.Column(db.Boolean, default=False)

    def generate_slug(self):
        _slug = unique_slug_generator(self)
        self.slug = _slug

    def __repr__(self):
        return self.id


class PartnerTitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    partners = db.relationship('Partner', backref='partnertitle', lazy=True)
