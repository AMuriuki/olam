from sqlalchemy.dialects.postgresql import UUID
import uuid
from app import db


class RecurringPlan(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), nullable=False)
    leads = db.relationship('Lead', backref='plans', lazy='dynamic')
