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
