from enum import unique
from app import db
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime

from app.utils import sku_generator

FILTERS = [
    ('0', 'Services'),
    ('1', 'Products'),
    ('2', 'Raw Materials'),
    ('3', 'Accessories'),
    ('4', 'Refurbished Laptops'),
    ('5', 'New Laptop'),
    ('6', 'Desktop PC'),
    ('6', 'Published'),
    ('7', 'Available in POS'),
    ('8', 'Can be sold'),
]


# class ProductManufacturer(db.Model):
#     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = db.Column(db.String(255), nullable=False)
#     products = db.relationship('Product', backref='manufacturer', lazy=True)


# class ProductModel(db.Model):
#     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = db.Column(db.String(255), nullable=False)
#     products = db.relationship('Product', backref='model', lazy=True)


class Product(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255))
    # manufacturer_id = db.Column(
    #     UUID(as_uuid=True), db.ForeignKey('product_manufacturer.id'), nullable=True)
    # model_id = db.Column(
    #     UUID(as_uuid=True), db.ForeignKey('product_model.id'), nullable=True)
    cost = db.Column(db.Float())
    price = db.Column(db.Float())
    tax_rate = db.Column(db.Float())
    category_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('product_category.id'))
    # screen_size = db.Column(db.String(10), index=True)
    # screen = db.Column(db.String(50), index=True)
    # processor_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
    #     'processor.id'), nullable=True)
    # memory_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
    #     'memory.id'), nullable=True)
    # storage_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
    #     'storage.id'), nullable=True)
    # gpu = db.Column(db.String(50), index=True)
    # os = db.Column(db.String(50), index=True)
    # os_version = db.Column(db.String(50), index=True)
    # weight = db.Column(db.String(50), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_for_sale_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    deleted_on = db.Column(db.DateTime, nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    approved_for_sale = db.Column(db.Boolean, default=False)
    in_stock = db.Column(db.Boolean, default=False)
    sku = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.Text())
    # color = db.Column(db.String(50), index=True)

    def generate_sku(self):
        _sku = sku_generator(self)
        self.sku = _sku


class ProductCategory(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), index=True)
    description = db.Column(db.Text())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    deleted_on = db.Column(db.DateTime, nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    products = db.relationship(
        'Product', backref='category', lazy='dynamic')


class ProductType(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), index=True)


class ProductAttribute(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), index=True)
    values = db.relationship('ProductAttributeValue',
                             backref='attribute', lazy=True)


class ProductAttributeValue(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), index=True)
    attribute_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'product_attribute.id'), nullable=True)
