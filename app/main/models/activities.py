from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Activity(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(120), index=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
