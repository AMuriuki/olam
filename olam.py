from unittest import result
from sqlalchemy.sql.elements import or_
from app.auth.models.user import Access, Group, Permission, Users
from app.crm.models.crm_stage import Stage
from app.main.models.country import Country
from app.main.models.partner import Partner
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
def inject_modules():
    modules = Module.query.all()
    if modules:
        return dict(modules=modules)
    else:
        return dict(modules="")


@app.context_processor
def partners():
    partners = db.session.query(Partner).filter(or_(
        Partner.is_company == True, Partner.is_individual == True)).all()
    if partners:
        return dict(partners=partners)
    else:
        return dict(partners="")


@app.context_processor
def stages():
    stages = Stage.query.filter_by(is_deleted=False).order_by('position').all()
    if stages:
        return dict(stages=stages)
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
    count = Lead.query.filter_by(stage_id=value).count()
    return count


@app.template_filter()
def get_user_name(value):
    user = Users.query.filter_by(id=value).first()
    user_details = Partner.query.filter_by(id=user.partner_id).first()
    return user_details.name


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
def contains(filter, selected):
    if filter in selected:
        return True


@app.template_filter()
def permission(value):
    permission = Permission
    return permission(value).name


@app.template_filter()
def view_access(value):
    pass
