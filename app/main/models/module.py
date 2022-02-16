import enum
import os
import csv
from app.models import PaginatedAPIMixin
from app.utils import unique_slug_generator
from config import basedir
from app import db, current_app
import logging


module_models = db.Table(
    'ModuleModels',
    db.Column('module_id', db.Integer, db.ForeignKey(
        'module.id'), primary_key=True),
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True))


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    technical_name = db.Column(db.String(128), index=True)  # technical name
    official_name = db.Column(db.String(128), index=True)  # official name
    bp_name = db.Column(db.String(128), index=True)  # blueprint name
    installed_version = db.Column(db.String(60))
    auto_install = db.Column(db.Boolean, default=False)
    state = db.Column(db.String(60))
    icon = db.Column(db.String(60))  # icon url
    enable = db.Column(db.Boolean, default=True)
    summary = db.Column(db.String(350))
    category_id = db.Column(db.Integer, db.ForeignKey('module_category.id'))
    usergroups = db.relationship('Group', backref='module', lazy='dynamic')
    user_groups_api = db.Column(db.Text)
    models_api = db.Column(db.Text)


class ModuleCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    modules = db.relationship('Module', backref='category', lazy='dynamic')


class Model(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    accessrights = db.relationship('Access', backref='model', lazy='dynamic')
    slug = db.Column(db.Text(), unique=True)

    def generate_slug(self):
        _slug = unique_slug_generator(self)
        self.slug = _slug

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slug': self.slug
        }
        return data
