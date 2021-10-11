from operator import index
from app import db, current_app
from config import basedir
import os
import csv
import logging
from datetime import datetime, timedelta

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]

FILTERS = [
    ('0', 'My Pipeline'),
    ('1', 'Unassigned'),
    ('2', 'Open Opportunities'),
    ('3', 'Lost Opportunities'),
    ('4', 'Won Opportunities'),
]


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('recurring_plan.id'))
    referred_by = db.Column(db.String(120))
    description = db.Column(db.Text())
    active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.String(15), index=True)
    partner_id = db.Column(db.Integer, db.ForeignKey('partner.id'))
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'))
    expected_revenue = db.Column(db.String(60))
    date_open = db.Column(db.DateTime, default=datetime.now)
    partner_email = db.Column(db.String(120), index=True)
    partner_phone = db.Column(db.String(60), index=True)
    partner_currency = db.Column(db.String(10), index=True)
    is_deleted = db.Column(db.Boolean, default=False)

    @staticmethod
    def insert_leads():
        csv_file = os.path.join(
            basedir, 'app/crm/data/leads.csv')
        with open(csv_file, 'r') as fin:
            dr = csv.DictReader(fin)
            current_app.logger.setLevel(logging.INFO)
            current_app.logger.info('seeding leads table')
            for i in dr:
                print(i)
                exists = db.session.query(
                    Lead.id).filter_by(id=i['lead_id']).first() is not None
                if exists:
                    pass
                else:
                    lead = Lead(
                        id=i['lead_id'], name=i['name'], user_id=i['user_id'], company_id=i['company_id'], referred_by=i['referred_by'], description=i['description'], active=True if i['active'] == 1 else False, priority=i['priority'], partner_id=i['partner_id'], stage=i['stage'], expected_revenue=i['expected_revenue'], partner_name=i['partner_name'], partner_email=i['partner_email'], partner_currency=i['partner_currency'])
                    db.session.add(lead)
            db.session.commit()
