from app import db
from app.main.models.activities import Activity
from app.utils import unique_slug_generator
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Medium'),
    ('2', 'High'),
    ('3', 'Very High'),
]

FILTERS = [
    ('M', 'My Pipeline'),
    ('U', 'Unassigned')
]


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=None)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('recurring_plan.id'))
    referred_by = db.Column(db.String(120))
    description = db.Column(db.Text())
    active = db.Column(db.Boolean, default=True)
    priority = db.Column(db.String(15), index=True)
    partner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('partner.id'))
    stage_id = db.Column(db.Integer, db.ForeignKey('stage.id'))
    expected_revenue = db.Column(db.String(60))
    date_open = db.Column(db.DateTime, default=datetime.utcnow)
    expected_closing = db.Column(db.DateTime, nullable=True)
    partner_email = db.Column(db.String(120), index=True)
    partner_phone = db.Column(db.String(60), index=True)
    partner_currency = db.Column(db.String(10), index=True)
    is_deleted = db.Column(db.Boolean, default=False)
    slug = db.Column(db.Text(), unique=True)
    notes = db.relationship('Note', backref='lead', lazy='dynamic')
    activities = db.relationship('LeadActivity', backref='lead', lazy='dynamic')

    def generate_slug(self):
        _slug = unique_slug_generator(self)
        self.slug = _slug


class LeadActivity(Activity):
    __table_args__ = {'extend_existing': True}
    id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'activity.id'), primary_key=True)
    lead_id = db.Column(
        db.Integer, db.ForeignKey('lead.id'), nullable=True)
