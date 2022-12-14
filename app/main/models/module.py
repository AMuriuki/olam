from app.models import PaginatedAPIMixin
from app.utils import unique_slug_generator
from app import db
from flask.helpers import url_for


module_models = db.Table(
    'ModuleModels',
    db.Column('module_id', db.Integer, db.ForeignKey(
        'module.id'), primary_key=True),
    db.Column('model_id', db.Integer, db.ForeignKey('model.id'), primary_key=True))


class Module(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    technical_name = db.Column(db.String(128), index=True)  # technical name
    official_name = db.Column(db.String(128), index=True)  # official name
    bp_name = db.Column(db.String(128), index=True)  # blueprint name
    installed_version = db.Column(db.String(60))
    auto_install = db.Column(db.Boolean, default=False)
    state = db.Column(db.String(60))
    icon = db.Column(db.String(60))  # icon url
    enable = db.Column(db.Boolean, default=True)
    summary = db.Column(db.String(350))
    category_id = db.Column(db.Integer, db.ForeignKey('module_category.id'))
    usergroups = db.relationship('Group', backref='module', lazy='dynamic')
    user_groups_api = db.Column(db.Text)
    models_api = db.Column(db.Text)
    url = db.Column(db.String(120))
    models = db.relationship(
        'Model', backref='module', lazy='dynamic')
    teams = db.relationship('PartnerTeam', backref='app', lazy='dynamic')
    activities = db.relationship('Activity', backref='module', lazy='dynamic')

    def to_dict(self):
        category = ModuleCategory.query.filter_by(id=self.category_id).first()
        data = {
            'id': self.id,
            'technical_name': self.technical_name,
            'bp_name': self.bp_name,
            'official_name': self.official_name,
            'summary': self.summary,
            'category_id': self.category_id,
            'category_name': category.name,
            'url': self.url
        }
        return data


class ModuleCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    modules = db.relationship('Module', backref='category', lazy='dynamic')


class Model(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    description = db.Column(db.String(128))
    accessrights = db.relationship('Access', backref='model', lazy='dynamic')
    activities = db.relationship('Activity', backref='model', lazy='dynamic')
    slug = db.Column(db.Text(), unique=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    teams = db.relationship('PartnerTeam', backref='model', lazy='dynamic')

    def generate_slug(self):
        _slug = unique_slug_generator(self)
        self.slug = _slug

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'slug': self.slug
        }
        return data
