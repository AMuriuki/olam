from enum import unique
from operator import index
from app import db


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, index=True)
    leads = db.relationship('Lead', backref='stage', lazy='dynamic')

    def max_id():
        query = Stage.query.order_by(Stage.id.desc()).first()
        return query.id
