from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.main.models.product import Product


class ProductPurchase(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'product.id'))
    vendor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('partner.id'))
    purchase_order_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey('purchase.id'))
