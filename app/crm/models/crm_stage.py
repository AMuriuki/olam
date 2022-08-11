from enum import unique
from operator import index
from app import db
from app.utils import get_random_color


class Stage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, index=True)
    leads = db.relationship('Lead', backref='stage', lazy='dynamic')
    position = db.Column(db.Integer, unique=True)
    is_deleted = db.Column(db.Boolean, default=False)
    color_badge = db.Column(db.String(120), default=get_random_color)

    def max_id():
        query = Stage.query.order_by(Stage.id.desc()).first()
        return query.id

    def max_postion():
        query = Stage.query.order_by(
            Stage.position.desc()).first()
        return query.position

    def first_position():
        query = Stage.query.order_by(
            Stage.position).first()
        return query.position
