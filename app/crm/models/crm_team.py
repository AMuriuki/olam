from enum import unique

from sqlalchemy.orm import backref
from app import db


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    leader = db.Column(db.Integer, db.ForeignKey('partner.id'))  # team leader
    members = db.relationship('TeamMember', backref='_team', lazy='dynamic')


class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.Integer, db.ForeignKey('partner.id'))
    team = db.Column(db.Integer, db.ForeignKey('team.id'))
