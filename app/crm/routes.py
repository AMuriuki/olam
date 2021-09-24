from flask_login import login_required
from flask import render_template
from app.crm import bp
from app.main.models.module import Module
from flask_babel import _, get_locale


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    modules = Module.query.all()
    return render_template('crm/index.html', title=_('CRM | Olam ERP'), modules=modules)


@bp.route('/pipeline', methods=['GET', 'POST'])
@login_required
def pipeline():
    modules = Module.query.all()
    return render_template('crm/pipeline.html', title=_('CRM Pipeline | Olam ERP'))


@bp.route('/sales', methods=['GET', 'POST'])
@login_required
def sales():
    modules = Module.query.all()
    pass


@bp.route('/reporting', methods=['GET', 'POST'])
@login_required
def reporting():
    modules = Module.query.all()
    pass


@bp.route('/configuration', methods=['GET', 'POST'])
@login_required
def configuration():
    modules = Module.query.all()
    pass
