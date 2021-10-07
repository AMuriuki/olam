from enum import unique

from sqlalchemy.orm import backref
from app import db
from app.models import PaginatedAPIMixin


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, unique=True)
    code = db.Column(db.String(60), index=True, unique=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    cities = db.relationship('City', backref='country', lazy='dynamic')
    calling_code = db.Column(db.String(120), index=True)
    currency_name = db.Column(db.String(60), index=True)
    currency_alphabetic_code = db.Column(db.String(60), index=True)
    currency_numeric_code = db.Column(db.Integer, index=True)
    languages = db.Column(db.String(120), index=True)
    partners = db.relationship('Partner', backref='country', lazy='dynamic')


class City(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    geonameid = db.Column(db.Integer, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    partners = db.relationship('Partner', backref='city', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name
        }
        return data


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, unique=True)
    code = db.Column(db.String(60), index=True)
