from calendar import c
from unittest import result
from sqlalchemy.sql.elements import or_
from app.auth.models.user import Access, Group, Permission, Users
from app.crm.models.crm_stage import Stage
from app.main.models.activities import Activity, ActivityType
from app.main.models.company import Company
from app.main.models.country import Country
from app.main.models.partner import Partner
from app.main.models.product import AttributeValue, ProductAttributeValue
from app.models import Task
from app.tasks import ManageTasks
from flask_migrate import upgrade
from app import create_app, cli, db
from app.main.models.module import Module
from app.crm.models.crm_lead import Lead
from flask_login import current_user

from app.utils import has_access


app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db}


@app.context_processor
def inject_activities():
    activities = Activity.query.distinct(
        Activity.model_id).group_by(Activity.id).all()
    if activities:
        return dict(_activities=activities)
    else:
        return dict(_activities="")


@app.context_processor
def inject_modules():
    modules = Module.query.all()
    if modules:
        return dict(modules=modules)
    else:
        return dict(modules="")


@app.context_processor
def inject_activity_types():
    activity_types = ActivityType.query.all()
    if activity_types:
        return dict(activity_types=activity_types)
    else:
        return dict(activity_types="")


@app.context_processor
def inject_companies():
    companies = Partner.query.filter_by(is_company=True).all()
    if companies:
        return dict(companies=companies)
    else:
        return dict(companies="")


@app.context_processor
def inject_currencies():
    query = db.session.query(
        Country.currency_alphabetic_code.distinct().label("currency_alphabetic_code")).order_by(
        'currency_alphabetic_code')
    currencies = [row.currency_alphabetic_code for row in query.all()]
    if currencies:
        return dict(currencies=currencies)
    else:
        return dict(currencies="")


@app.context_processor
def partners():
    partners = db.session.query(Partner).filter(or_(
        Partner.is_company == True, Partner.is_individual == True)).all()
    if partners:
        return dict(partners=partners)
    else:
        return dict(partners="")


@app.context_processor
def company():
    company = db.session.query(Company).first()
    if company:
        return dict(company=company)
    else:
        return dict(company="")


@app.context_processor
def stages():
    stagesids = []
    stages = Stage.query.filter_by(is_deleted=False).order_by('position').all()
    for stage in stages:
        stagesids.append(stage.id)
    if stages:
        return dict(stages=stages, stage_ids=stagesids)
    else:
        return dict(stages="")


@app.context_processor
def max_stage_position():
    query = Stage.query.filter_by(is_deleted=False).order_by(
        Stage.position.desc()).first()
    if query:
        return dict(max_stage_position=query.position)
    else:
        return dict(max_stage_position="")


@app.context_processor
def first_stage_position():
    query = Stage.query.filter_by(is_deleted=False).order_by(
        Stage.position).first()
    if query:
        return dict(first_stage_position=query.position)
    else:
        return dict(first_stage_position="")


@app.context_processor
def user():
    if current_user.is_authenticated:
        user = Users.query.filter_by(id=current_user.get_id()).first()
        if user:
            user_country = Country.query.filter_by(
                code=user.country_code).first()
            if user_country:
                user_currency = user_country.currency_alphabetic_code
            else:
                user_currency = ""
        else:
            user_country = ""

        return dict(user=user, user_country=user_country, user_currency=user_currency)
    else:
        return dict(user="", user_country="", user_currency="")


@app.context_processor
def sales_people():
    sales_people = Partner.query.filter_by(is_tenant=True).order_by('id').all()
    if sales_people:
        return dict(sales_people=sales_people)
    else:
        return dict(sales_people="")


@app.context_processor
def users():
    users = Partner.query.filter_by(is_tenant=True).order_by('id').all()
    if users:
        return dict(users=users)
    else:
        return dict(sales_people="")


@app.before_first_request
def seed_database():
    exists = Task.query.filter_by(name='seed_database').first()
    if not exists:
        ManageTasks.launch_task('seed_database', ('Seeding DB...'))
        db.session.commit()


@app.template_filter()
def numberFormat(value):
    return "{:,.2f}".format(value)


@app.template_filter()
def stringChars(value):
    words = value.split()
    letters = [word[0] for word in words]
    return "".join(letters)


@app.template_filter()
def get_pipeline_count(value):
    count = Lead.query.filter_by(stage_id=value).filter_by(
        user_id=current_user.get_id()).filter_by(is_deleted=False).count()
    return count


@app.template_filter()
def get_user_name(value):
    if value:
        user = Users.query.filter_by(id=value).first()
        user_details = Partner.query.filter_by(id=user.partner_id).first()
        return user_details.name
    else:
        return None


@app.template_filter()
def installed(value):
    module = Module.query.filter_by(id=value).first()
    return module


@app.template_filter()
def partner_name(value):
    partner = Partner.query.filter_by(id=value).first()
    return partner.name if partner.name else partner.company_name


@app.template_filter()
def remove_hyphens(string):
    if string:
        return string.replace('-', ' ')
    else:
        return None


@app.template_filter()
def can_view_module(module_id):
    access_groups = [g.id for g in Group.query.filter_by(module_id=module_id)]
    user_groups = [g.id for g in current_user.groups]
    L1 = set(access_groups)
    L2 = set(user_groups)
    result = L1.intersection(L2)
    return has_access(result)


@app.template_filter()
def has(user_id, group_id):
    user = Users.query.filter_by(id=user_id).first()
    user_groups = [g.id for g in user.groups]
    if group_id in user_groups:
        return True
    else:
        return False


@app.template_filter()
def can_view_model(user, model_id):
    access_groups = [g.id for g in Group.query.join(
        Access, Group.rights).filter_by(model_id=model_id)]
    user_groups = [g.id for g in user.groups]
    L1 = set(access_groups)
    L2 = set(user_groups)
    result = L1.intersection(L2)
    return has_access(result)


@app.template_filter()
def can_create(user, model_id):
    access_groups = [g.id for g in Group.query.join(
        Access, Group.rights).filter_by(model_id=model_id).filter_by(create=True)]
    user_groups = [g.id for g in user.groups]
    L1 = set(access_groups)
    L2 = set(user_groups)
    result = L1.intersection(L2)
    return has_access(result)


@app.template_filter()
def can_write(user, model_id):
    access_groups = [g.id for g in Group.query.join(
        Access, Group.rights).filter_by(model_id=model_id).filter_by(write=True)]
    user_groups = [g.id for g in user.groups]
    L1 = set(access_groups)
    L2 = set(user_groups)
    result = L1.intersection(L2)
    return has_access(result)


@app.template_filter()
def can_delete(user, model_id):
    access_groups = [g.id for g in Group.query.join(
        Access, Group.rights).filter_by(model_id=model_id).filter_by(delete=True)]
    user_groups = [g.id for g in user.groups]
    L1 = set(access_groups)
    L2 = set(user_groups)
    result = L1.intersection(L2)
    return has_access(result)


@app.template_filter()
def contains(filter, selected):
    if filter in selected:
        return True


@app.template_filter()
def permission(value):
    permission = Permission
    return permission(value).name


@app.template_filter()
def can_read(user, model_id):
    access_groups = [g.id for g in Group.query.join(
        Access, Group.rights).filter_by(model_id=model_id).filter_by(read=True)]
    user_groups = [g.id for g in user.groups]
    L1 = set(access_groups)
    L2 = set(user_groups)
    result = L1.intersection(L2)
    return has_access(result)


@app.template_filter()
def no_activities(value):
    count = Activity.query.filter_by(model_id=value).count()
    return count


@app.template_filter()
def contact_name(value):
    parent = Partner.query.filter_by(id=str(value)).first()
    child = Partner.query.filter_by(parent_id=parent.id).first()
    return child.name


@app.template_filter()
def contact_email(value):
    parent = Partner.query.filter_by(id=str(value)).first()
    child = Partner.query.filter_by(parent_id=parent.id).first()
    return child.email


@app.template_filter()
def contact_phone(value):
    parent = Partner.query.filter_by(id=str(value)).first()
    child = Partner.query.filter_by(parent_id=parent.id).first()
    return child.phone_no


@app.template_filter()
def contact_position(value):
    parent = Partner.query.filter_by(id=str(value)).first()
    child = Partner.query.filter_by(parent_id=parent.id).first()
    return child.function


@app.template_filter()
def product_model(value):
    attribute = ProductAttributeValue.query.filter_by(
        product_id=value, attribute_id='96f65155-e8e3-4680-93bf-f305275062a7').first()
    if attribute:
        value_id = attribute.attribute_value_id
        value = AttributeValue.query.filter_by(id=value_id).first()
        return value.name


@app.template_filter()
def get_model(group_id):
    group = Group.query.filter_by(id=group_id).first()
    access = group.rights
    for access in access:
        return access.name
