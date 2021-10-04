from flask_login import login_required
from flask import render_template
from app.crm import bp
from app.crm.models.crm_lead import Lead
from app.main.models.module import Module
from flask_babel import _, get_locale
from app import db
from app.auth.models.user import User
from app.main.models.partner import Partner
from app.main.models.company import Company
from sqlalchemy import or_
from app.contacts.forms import TITLES, BasicCompanyInfoForm, BasicIndividualInfoForm


@bp.route('/', methods=['GET', 'POST'])
@login_required
def pipeline():
    form1 = BasicCompanyInfoForm()
    form2 = BasicIndividualInfoForm()
    pipeline = Lead.query.all()
    titles = TITLES
    partners = db.session.query(Partner).filter(or_(
        Partner.is_company == True, Partner.is_individual == True)).all()
    companies = Partner.query.filter_by(is_company=True).all()
    return render_template('crm/pipeline.html', title=_('CRM Pipeline | Olam ERP'), pipeline=pipeline, partners=partners, form1=form1, form2=form2, companies=companies, titles=titles)


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
