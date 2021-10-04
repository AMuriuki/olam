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
    return dict(modules=modules)


@app.before_first_request
def seed_database():
    ManageTasks.launch_task('seed_database', ('Seeding DB...'))
    db.session.commit()


@app.template_filter()
def numberFormat(value):
    return "{:,.2f}".format(value)


@app.template_filter()
def get_pipeline_count(value):
    count = Lead.query.filter_by(stage=value).count()
    return count
