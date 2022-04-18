import imp
from sqlalchemy import null
from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid
from datetime import datetime
from app.main.models.activities import Activity
from app.main.models.partner import Partner
from app.utils import generate_reference, purchase_reference_generator
from sqlalchemy.dialects.postgresql import TIMESTAMP


FILTERS = [
    ('0', 'My Purchases'),
    ('1', 'Starred'),
    ('2', 'RFQs'),
    ('3', 'Purchase Orders'),
    ('4', 'To Approve'),
    ('5', 'Order Date'),
    ('6', 'Draft RFQs'),
    ('7', 'Waiting RFQs')
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
    time = db.Column(db.String(10), nullable=True)
    total = db.Column(db.String(120), index=True)
    status = db.Column(UUID(as_uuid=True), db.ForeignKey('purchase_status.id'))
    activity = db.relationship(
        'PurchaseActivity', backref='purchase', lazy=True, uselist=False)
    description = db.Column(db.Text())
    unit_price = db.Column(db.Float())
    quantity = db.Column(db.Integer())
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime)
    products = db.relationship(
        'ProductPurchase', backref='purchase_order', lazy='dynamic')

    def generate_reference(self):
        _reference = purchase_reference_generator(self)
        self.reference = _reference

    def to_dict(self):
        vendor = Partner.query.filter_by(id=self.vendor).first()
        data = {
            'id': self.id,
            'reference': self.reference,
            'vendor_name': vendor.get_name(),
            'vendor': self.vendor,
            'due_date': self.due_date,
        }
        return data


class PurchaseActivity(Activity):
    __table_args__ = {'extend_existing': True}
    id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'activity.id'), primary_key=True)
    purchase_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('purchase.id'), nullable=True)
