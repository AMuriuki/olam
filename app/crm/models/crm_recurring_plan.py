from sqlalchemy.orm import backref
from app import db


class RecurringPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(120), nullable=False)
    leads = db.relationship('Lead', backref='plans', lazy='dynamic')

    def max_id():
        query = RecurringPlan.query.order_by(RecurringPlan.id.desc()).first()
        return query.id
