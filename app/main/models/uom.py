from enum import unique
from app import db
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid


class Uom(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), nullable=False, unique=True)
    category_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('uom_category.id'))
    products = db.relationship(
        'Product', backref='uom', lazy='dynamic')


class UomCategory(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), nullable=False)
    uoms = db.relationship('Uom', backref='category', lazy=True)
