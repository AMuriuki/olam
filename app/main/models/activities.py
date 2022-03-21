from sqlalchemy import null
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Activity(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    summary = db.Column(db.String(300), index=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=True)
    activity_type = db.Column(
        UUID(as_uuid=True), db.ForeignKey('activity_type.id'))
    due_date = db.Column(db.Date)
    assigned_to = db.Column(UUID(as_uuid=True), db.ForeignKey('partner.id'))
    notes = db.Column(db.Text())

    def __repr__(self):
        return str(self.id)


class ActivityType(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), index=True)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    activities = db.relationship('Activity', backref='type', lazy='dynamic')
