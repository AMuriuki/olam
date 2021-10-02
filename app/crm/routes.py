from flask_login import login_required
from flask import render_template
from app.crm import bp
from app.main.models.module import Module
from flask_babel import _, get_locale


@bp.route('/', methods=['GET', 'POST'])
@login_required
def pipeline():

    return render_template('crm/pipeline.html', title=_('CRM Pipeline | Olam ERP'))


@bp.route('/pipeline', methods=['GET', 'POST'])
@login_required
def empty():

    return render_template('crm/pipeline.html', title=_('CRM Pipeline | Olam ERP'))


@bp.route('/sales', methods=['GET', 'POST'])
@login_required
def sales():

    pass


@bp.route('/reporting', methods=['GET', 'POST'])
@login_required
def reporting():

    pass


@bp.route('/configuration', methods=['GET', 'POST'])
@login_required
def configuration():

    pass
