from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid

from app.main.models.activities import Activity


FILTERS = [
    ('0', 'My Purchases'),
    ('1', 'Starred'),
    ('3', 'RFQs'),
    ('4', 'Purchase Orders'),
    ('5', 'To Approve'),
    ('6', 'Order Date'),
    ('7', 'Draft RFQs'),
    ('8', 'Waiting RFQs'),
    ('9', 'My Purchases'),
]


class PurchaseFilters(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    index = db.Column(db.Integer, index=True, unique=True)
    name = db.Column(db.String(120), index=True, unique=True)


class PurchaseStatus(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), index=True, unique=True)
    purchases = db.relationship(
        'Purchase', backref='purchase_status', lazy='dynamic')


class Purchase(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference = db.Column(db.String(120), index=True, unique=True)
    vendor = db.Column(UUID(as_uuid=True), db.ForeignKey('partner.id'))
    representative = db.Column(db.Integer, db.ForeignKey('users.id'))
    due_date = db.Column(db.Date)
    total = db.Column(db.String(120), index=True)
    status = db.Column(UUID(as_uuid=True), db.ForeignKey('purchase_status.id'))
    activities = db.relationship(
        'PurchaseActivity', backref='lead', lazy='dynamic')


class PurchaseActivity(Activity):
    __table_args__ = {'extend_existing': True}
    id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'activity.id'), primary_key=True)
    purchase_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('purchase.id'), nullable=True)
