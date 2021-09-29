from datetime import datetime
from app import db


class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    title = db.Column(db.String(60), index=True)
    company_name = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    function = db.Column(db.String(60), index=True)
    date_added = db.Column(db.DateTime, default=datetime.now)
    is_individual = db.Column(db.Boolean, default=False)
    is_company = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    title_id = db.Column(db.Integer, db.ForeignKey('partner_title.id'))
    phone_no = db.Column(db.String(120), index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    parent = db.relationship('Partner', remote_side=[id])
    website = db.Column(db.String(120), index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    users = db.relationship('User', backref='partner', lazy='dynamic')
    is_tenant = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.company_name


class PartnerTitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    partners = db.relationship('Partner', backref='partnertitle', lazy=True)
