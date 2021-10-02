from operator import index
from app import db

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    referred_by = db.Column(db.String(120))
    description = db.Column(db.Text())
    active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.String(15), index=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
