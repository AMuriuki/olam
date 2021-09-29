from enum import unique
from app import db


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, unique=True)
    code = db.Column(db.String(60), index=True, unique=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    cities = db.relationship('City', backref='country', lazy='dynamic')
    calling_code = db.Column(db.Integer, index=True)
    currency_name = db.Column(db.String(60), index=True)
    currency_alphabetic_code = db.Column(db.String(60), index=True)
    currency_numeric_code = db.Column(db.Integer, index=True)
    languages = db.Column(db.String(60), index=True)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    geonameid = db.Column(db.Integer, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, unique=True)
    code = db.Column(db.String(60), index=True)
