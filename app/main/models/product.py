from enum import unique
from itertools import product
from app import db
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from app.models import PaginatedAPIMixin

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


class ProductAttributeValue(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('product.id'))
    attribute_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('product_attribute.id'))
    attribute_value_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('attribute_value.id'))
    attribute_value = db.relationship('AttributeValue')
    product_attribute = db.relationship('ProductAttribute')
    product = db.relationship('Product')


class Product(PaginatedAPIMixin, db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), unique=True)
    cost = db.Column(db.Float())
    price = db.Column(db.Float())
    total_price = db.Column(db.Float())
    # tax_rate = db.Column(db.Float())
    category_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('product_category.id'))
    type_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('product_type.id'))
    uom_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('uom.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_for_sale_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    deleted_on = db.Column(db.DateTime, nullable=True)
    deleted = db.Column(db.Boolean, default=False)
    published = db.Column(db.Boolean, default=False)
    approved_for_sale = db.Column(db.Boolean, default=False)
    in_stock = db.Column(db.Boolean, default=False)
    sku = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.Text())
    quantity = db.Column(db.String(20))
    tax = db.Column(db.String(50), index=True)

    def generate_sku(self):
        _sku = sku_generator(self)
        self.sku = _sku

    def to_dict(self):
        attributes = ProductAttributeValue.query.filter_by(
            product_id=self.id).all()
        data = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'total_price': self.total_price,
            'tax_rate': self.tax,
            'category': self.category.name,
            'type': self.type.name,
            'uom': self.uom.name,
            'quantity': self.quantity,
            'description': self.description,
            'attributes': [
                {
                    attribute.product_attribute.name: attribute.attribute_value.name,
                } for attribute in attributes
            ]
        }
        return data


class ProductCategory(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), index=True, unique=True)
    slug = db.Column(db.String(120), index=True, unique=True)
    parent_id = db.Column(UUID(as_uuid=True),
                          db.ForeignKey('product_category.id'))
    parent = db.relationship('ProductCategory', remote_side=[id])
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
    products = db.relationship(
        'Product', backref='type', lazy='dynamic')


class ProductAttribute(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), index=True, unique=True)
    index = db.Column(db.Integer, unique=True)
    values = db.relationship('AttributeValue', backref='attribute', lazy=True)
    product_attribute_values = db.relationship(
        'ProductAttributeValue', backref='attribute', lazy=True)


class AttributeValue(PaginatedAPIMixin, db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), index=True, unique=True)
    attribute_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'product_attribute.id'), nullable=True)
    product_attribute_values = db.relationship(
        'ProductAttributeValue', backref='value', lazy=True)

    def to_dict(self):
        data = {
            'id': str(self.id),
            'name': self.name
        }
        return data
