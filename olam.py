from sqlalchemy.sql.elements import or_
from app.auth.models.user import Users
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
        return dict(modules=None)


@app.context_processor
def partners():
    partners = db.session.query(Partner).filter(or_(
        Partner.is_company == True, Partner.is_individual == True)).all()
    if partners:
        return dict(partners=partners)
    else:
        return dict(partners=None)


@app.context_processor
def stages():
    stages = Stage.query.filter_by(is_deleted=False).order_by('position').all()
    if stages:
        return dict(stages=stages)
    else:
        return dict(stages=None)


@app.context_processor
def max_stage_position():
    query = Stage.query.filter_by(is_deleted=False).order_by(
        Stage.position.desc()).first()
    if query:
        return dict(max_stage_position=query.position)
    else:
        return dict(max_stage_position=None)


@app.context_processor
def first_stage_position():
    query = Stage.query.filter_by(is_deleted=False).order_by(
        Stage.position).first()
    if query:
        return dict(first_stage_position=query.position)
    else:
        return dict(first_stage_position=None)


@app.context_processor
def user():
    if current_user.is_authenticated:
        user = Users.query.filter_by(id=current_user.get_id()).first()
        user_country = Country.query.filter_by(code=user.country_code).first()
        user_currency = user_country.currency_alphabetic_code
        return dict(user=user, user_country=user_country, user_currency=user_currency)
    else:
        return dict(user=None, user_country=None, user_currency=None)


@app.context_processor
def sales_people():
    sales_people = Partner.query.filter_by(is_tenant=True).order_by('id').all()
    if sales_people:
        return dict(sales_people=sales_people)
    else:
        return dict(sales_people=None)


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
def partner_name(value):
    partner = Partner.query.filter_by(id=value).first()
    return partner.name if partner.name else partner.company_name
