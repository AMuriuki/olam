from datetime import datetime
from enum import unique
import hashlib

from sqlalchemy.orm import backref
from app import db
from app.utils import unique_slug_generator
from sqlalchemy.dialects.postgresql import UUID
import uuid


partner_roles = db.Table(
    'PartnerRoles',
    db.Column('partner_id', UUID(as_uuid=True), db.ForeignKey(
        'partner.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('partner_role.id'), primary_key=True))

partner_teams = db.Table(
    'PartnerTeams',
    db.Column('partner_id', UUID(as_uuid=True), db.ForeignKey(
        'partner.id'), primary_key=True),
    db.Column('team_id', db.Integer, db.ForeignKey('partner_team.id'), primary_key=True))


class Partner(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), index=True)
    title = db.Column(db.String(60), index=True)
    company_name = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True)
    function = db.Column(db.String(60), index=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    dob = db.Column(db.Date)
    is_individual = db.Column(db.Boolean, default=False)
    is_company = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    phone_no = db.Column(db.String(120), index=True)
    parent_id = db.Column(UUID(as_uuid=True), db.ForeignKey('partner.id'))
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
    roles = db.relationship(
        'PartnerRole', secondary=partner_roles, back_populates="partners")
    teams = db.relationship(
        'PartnerTeam', secondary=partner_teams, back_populates="members")
    slug = db.Column(db.Text(), unique=True)
    is_archived = db.Column(db.Boolean, default=False)
    contact_person = db.Column(db.Boolean, default=False)
    assigned_activities = db.relationship(
        'Activity', backref='assignee', lazy='dynamic')

    def generate_slug(self):
        _slug = unique_slug_generator(self)
        self.slug = _slug

    def __repr__(self):
        return str(self.id)


class PartnerRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    partners = db.relationship(
        'Partner', secondary=partner_roles, back_populates="roles")


class PartnerTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    leader = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'partner.id'))  # team leader
    token = db.Column(db.String(120), index=True, unique=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    members = db.relationship(
        'Partner', secondary=partner_teams, back_populates="teams")

    def set_token(self, partner_id):
        hash_object = hashlib.sha1((str.encode(str(partner_id))))
        hex_dig = hash_object.hexdigest()
        self.token = hex_dig
