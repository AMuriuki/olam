from enum import unique
import hashlib

from sqlalchemy.orm import backref
from app import db


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    leader = db.Column(db.Integer, db.ForeignKey('partner.id'))  # team leader
    members = db.relationship('TeamMember', backref='_team', lazy='dynamic')
    token = db.Column(db.String(120), index=True, unique=True)

    def set_token(self, partner_id):
        hash_object = hashlib.sha1((str.encode(str(partner_id))))
        hex_dig = hash_object.hexdigest()
        self.token = hex_dig


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.Integer, db.ForeignKey('partner.id'))
    team = db.Column(db.Integer, db.ForeignKey('team.id'))
