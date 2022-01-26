from app.main.models.partner import Partner
from app.main.models import company
import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
import os
import csv
from time import time
from flask import current_app, url_for, session
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import redis
import rq
from app import db, login_manager
from app.search import add_to_index, remove_from_index, query_index
from app.models import SearchableMixin, PaginatedAPIMixin, Task
from flask_login import UserMixin, current_user
from app.utils import unique_slug_generator
from config import basedir

from sqlalchemy import create_engine
from sqlalchemy.orm import backref, scoped_session, sessionmaker
from werkzeug.local import LocalProxy


import enum
import logging
import hashlib


access_rights = db.Table(
    'AccessRights',
    db.Column('group_id', db.Integer, db.ForeignKey(
        'group.id'), primary_key=True),
    db.Column('access_id', db.Integer, db.ForeignKey('access.id'), primary_key=True))

user_group = db.Table(
    'UserGroup',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True))


class Users(UserMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    token = db.Column(db.String(120), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=False)
    is_staff = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime, default=datetime.now)
    registered_on = db.Column(db.DateTime, default=datetime.now)
    password_hash = db.Column(db.String(128))
    leads = db.relationship('Lead', backref='owner', lazy='dynamic')
    country_code = db.Column(db.String(10), index=True)
    groups = db.relationship(
        'Group', secondary=user_group, back_populates="users")

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_token(self, partner_id):
        hash_object = hashlib.sha1((str.encode(str(partner_id))))
        hex_dig = hash_object.hexdigest()
        self.token = hex_dig

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    def get_database_activation_token(self, expires_in=600):
        return jwt.encode(
            {'activate_database': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    def get_activation_token(self):
        return jwt.encode(
            {'activate': self.id},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Users.query.get(id)

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['activate']
        except:
            return
        return Users.query.get(id)

    @staticmethod
    def verify_database_activation_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['activate_database']
        except:
            return
        return Users.query.get(id)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'token': self.name,
            'token_expiration': self.token_expiration,
            'company_id': self.company_id,
            'is_active': self.is_active,
            'name': self.name,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'registered_on': self.registered_on.isoformat() + 'Z',
            'is_staff': self.is_staff,
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['name', 'email', 'token', 'token_expiration', 'company_id']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        now = datetime.now
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.now - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = Users.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.now:
            return None
        return user


@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    groups = db.relationship(
        'Group', secondary=access_rights, back_populates="rights")
    slug = db.Column(db.Text(), unique=True)
    read = db.Column(db.Boolean, default=False)
    write = db.Column(db.Boolean, default=False)
    create = db.Column(db.Boolean, default=False)
    delete = db.Column(db.Boolean, default=False)

    def generate_slug(self):
        _slug = unique_slug_generator(self)
        self.slug = _slug


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    users = db.relationship(
        'Users', secondary=user_group, back_populates="groups")
    slug = db.Column(db.Text(), unique=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    is_active = db.Column(db.Boolean, default=True)
    rights = db.relationship(
        'Access', secondary=access_rights, back_populates="groups")

    def generate_slug(self):
        _slug = unique_slug_generator(self)
        self.slug = _slug
