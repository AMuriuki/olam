from flask_login import login_required, current_user
from flask import json, render_template, session, jsonify, request, redirect, url_for
from app.crm import bp
from app.crm.models.crm_lead import Lead
from app.crm.models.crm_recurring_plan import RecurringPlan
from app.main.models.module import Module
from flask_babel import _, get_locale
from app import db
from app.auth.models.user import User
from app.main.models.partner import Partner
from app.main.models.company import Company
from sqlalchemy import log, or_
from app.contacts.forms import TITLES, BasicCompanyInfoForm, BasicIndividualInfoForm
from app.crm.forms import BoardItemForm, NewRecurringPlanForm
from app.main.models.country import Country


@login_required
@bp.route('/get_partner_details', methods=['GET', 'POST'])
def get_partner_details():
    partner = Partner.query.filter_by(id=request.form['partner_id']).first()
    return jsonify({"partner_email": partner.email, "partner_phone": partner.phone_no})


@login_required
@bp.route('/selected_priority', methods=['GET', 'POST'])
def select_priority():
    session['selected_priority'] = request.form['selected_priority']
    return jsonify({"response": "success"})


@login_required
@bp.route('/pipeline_stage', methods=['GET', 'POST'])
def pipeline_stage():
    session['pipeline_stage'] = request.form['pipeline_stage']
    return jsonify({"response": "success"})


@login_required
@bp.route('/new_company_contact', methods=['GET', 'POST'])
def new_company_contact():
    form1 = BasicCompanyInfoForm()
    if form1.validate_on_submit():
        partner = Partner(company_name=form1.companyname.data,
                          phone_no=form1.phonenumber.data, website=form1.website.data, is_company=True, is_active=True, email=form1.email.data)
        db.session.add(partner)
        db.session.commit()
        return jsonify({"response": "success", "partner_name": partner.company_name, "partner_id": partner.id})


@login_required
@bp.route('/new_individual_contact', methods=['GET', 'POST'])
def new_individual_contact():
    form2 = BasicIndividualInfoForm()
    if form2.validate_on_submit():
        partner = Partner(name=form2.name.data,
                          phone_no=form2.phonenumber.data, title=request.form['select_title'], parent_id=request.form['select_company'], website=form2.website.data, is_individual=True, is_active=True, function=form2.jobposition.data, email=form2.email.data)
        db.session.add(partner)
        db.session.commit()
        return jsonify({"response": "success", "partner_name": partner.name, "partner_id": partner.id})


@login_required
@bp.route('/new_recurring_plan', methods=['GET', 'POST'])
def new_recurring_plan():
    form4 = NewRecurringPlanForm()
    if form4.validate_on_submit():
        new_plan = RecurringPlan(name=request.form['name'])
        db.session.add(new_plan)
        db.session.commit()
        return jsonify({"plan_id": new_plan.id, "plan_name": new_plan.name})


@bp.route('/', methods=['GET', 'POST'])
@login_required
def pipeline():
    form1 = BasicCompanyInfoForm()
    form2 = BasicIndividualInfoForm()
    form3 = BoardItemForm()
    form4 = NewRecurringPlanForm()
    user = User.query.filter_by(id=current_user.get_id()).first()
    country_code = user.country_code
    user_country = Country.query.filter_by(code=country_code).first()
    user_currency = user_country.currency_alphabetic_code

    pipeline = Lead.query.all()

    plans = RecurringPlan.query.all()
    titles = TITLES
    partners = db.session.query(Partner).filter(or_(
        Partner.is_company == True, Partner.is_individual == True)).all()
    companies = Partner.query.filter_by(is_company=True).all()
    query = db.session.query(
        Country.currency_alphabetic_code.distinct().label("currency_alphabetic_code")).order_by(
        'currency_alphabetic_code')
    currencies = [row.currency_alphabetic_code for row in query.all()]
    if form3.validate_on_submit():

        opportunity = Lead(name=request.form['opportunity'],
                           user_id=current_user.get_id(), partner_id=request.form['pipeline_select_org'], priority=session['selected_priority'], stage=session['pipeline_stage'], expected_revenue=request.form['expected_revenue'], partner_email=request.form['partner_email'], partner_phone=request.form['partner_phone'], plan_id=request.form['recurring_plan'], partner_currency=request.form['_partner_currency'])
        db.session.add(opportunity)
        db.session.commit()
        return redirect(url_for('crm.pipeline'))

    return render_template('crm/pipeline.html', title=_('CRM Pipeline | Olam ERP'), pipeline=pipeline, partners=partners, form1=form1, form2=form2, form3=form3, companies=companies, titles=titles, currencies=currencies, user_currency=user_currency, plans=plans, form4=form4)


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
