from flask_login import login_required, current_user
from flask import json, render_template, session, jsonify, request, redirect, url_for, flash
from app.crm import bp
from app.crm.models.crm_lead import FILTERS, Lead
from app.crm.models.crm_recurring_plan import RecurringPlan
from app.crm.models.crm_stage import Stage
from app.crm.models.crm_team import Team
from app.main.models.module import Module
from flask_babel import _, get_locale
from app import db
from app.main.models.partner import Partner
from sqlalchemy import log, or_
from app.contacts.forms import TITLES, BasicCompanyInfoForm, BasicIndividualInfoForm
from app.crm.forms import AddStage, BoardItemForm, NewRecurringPlanForm, EditStageForm, CreateSalesTeamForm
from app.main.models.country import Country


@login_required
@bp.route('/edit_stage', methods=['GET', 'POST'])
def edit_stage():
    stage = Stage.query.filter_by(id=request.form['stage_id']).first()
    stage.name = request.form['stage_name']
    db.session.commit()
    return jsonify({"response": "success"})


@login_required
@bp.route('/delete_stage', methods=['GET', 'POST'])
def delete_stage():
    stage = Stage.query.filter_by(id=request.form['stage_id']).first()
    stage.is_deleted = True
    db.session.commit()
    return jsonify({"response": "success"})


@login_required
@bp.route('/move_stage_forward', methods=['GET', 'POST'])
def move_stage_forward():
    current_stage = Stage.query.filter_by(id=request.form['stage_id']).first()
    last_position = Stage.max_postion()
    current_position = current_stage.position
    next_position = current_position + 1
    next_stage = Stage.query.filter_by(
        position=next_position).filter_by(is_deleted=False).first()
    next_stage.position = last_position + 1
    db.session.commit()
    current_stage.position = next_position
    db.session.commit()
    next_stage.position = current_position
    db.session.commit()
    return jsonify({"response": "success"})


@login_required
@bp.route('/move_stage_behind', methods=['GET', 'POST'])
def move_stage_behind():
    current_stage = Stage.query.filter_by(id=request.form['stage_id']).first()
    first_position = Stage.first_position()
    current_position = current_stage.position
    previous_position = current_position - 1
    previous_stage = Stage.query.filter_by(
        position=previous_position).filter_by(is_deleted=False).first()
    previous_stage.position = first_position - 1
    db.session.commit()
    current_stage.position = previous_position
    db.session.commit()
    previous_stage.position = current_position
    db.session.commit()
    return jsonify({"response": "success"})


@login_required
@bp.route('/update_item', methods=['GET', 'POST'])
def update_item():
    opportunity = Lead.query.filter_by(id=request.form['item_id']).first()
    opportunity.priority = request.form['priority']
    db.session.commit()
    return jsonify({"response": "success"})


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
        partner.generate_slug()
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
        partner.generate_slug()
        db.session.add(partner)
        db.session.commit()
        return jsonify({"response": "success", "partner_name": partner.name, "partner_id": partner.id})


@login_required
@bp.route('/new_recurring_plan', methods=['GET', 'POST'])
def new_recurring_plan():
    form4 = NewRecurringPlanForm()
    if form4.validate_on_submit():
        max_id = RecurringPlan.max_id()
        new_plan = RecurringPlan(id=max_id+1, name=request.form['name'])
        db.session.add(new_plan)
        db.session.commit()
        return jsonify({"plan_id": new_plan.id, "plan_name": new_plan.name})
    return jsonify({"response": "failed"})


@bp.route('/', methods=['GET', 'POST'])
@login_required
def pipeline():
    form1 = BasicCompanyInfoForm()
    form2 = BasicIndividualInfoForm()
    form3 = BoardItemForm()
    form4 = NewRecurringPlanForm()
    form5 = EditStageForm()
    form6 = AddStage()

    

    pipeline = Lead.query.filter_by(
        user_id=current_user.get_id()).order_by(Lead.priority.desc()).all()

    plans = RecurringPlan.query.all()
    titles = TITLES
    filters = FILTERS
    new_stage = False

    companies = Partner.query.filter_by(is_company=True).all()
    query = db.session.query(
        Country.currency_alphabetic_code.distinct().label("currency_alphabetic_code")).order_by(
        'currency_alphabetic_code')
    currencies = [row.currency_alphabetic_code for row in query.all()]
    if form3.submit1.data and form3.validate_on_submit():
        opportunity = Lead(name=request.form['opportunity'], user_id=current_user.get_id(), partner_id=request.form['pipeline_select_org'], priority=session['selected_priority'], stage_id=int(
            session['pipeline_stage']), expected_revenue=request.form['expected_revenue'], partner_email=request.form['partner_email'], partner_phone=request.form['partner_phone'], plan_id=request.form['recurring_plan'], partner_currency=request.form['_partner_currency'])
        opportunity.generate_slug()
        db.session.add(opportunity)
        db.session.commit()
        return redirect(url_for('crm.pipeline'))

    if form6.submit6.data and form6.validate_on_submit():
        max_id = Stage.max_id()
        max_position = Stage.max_postion()
        stage = Stage(id=max_id+1, name=form6.name.data,
                      position=max_position+1)
        db.session.add(stage)
        db.session.commit()
        new_stage = True
        flash(_("New stage added successfully"))
        return redirect(url_for('crm.pipeline', new_stage=new_stage))

    return render_template('crm/pipeline.html', title=_('CRM Pipeline | Olam ERP'), pipeline=pipeline, form1=form1, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, companies=companies, titles=titles, currencies=currencies, plans=plans, filters=filters, new_stage=new_stage)


@bp.route('/pipeline', methods=['GET', 'POST'])
@login_required
def empty():
    return render_template('crm/pipeline.html', title=_('CRM Pipeline | Olam ERP'))


@bp.route('/sales', methods=['GET', 'POST'])
@login_required
def sales():
    pass


@bp.route('/sales_team', methods=['GET', 'POST'])
@login_required
def sales_teams():
    sales_teams = Team.query.join(Partner).all()
    for sales_team in sales_teams:
        print(sales_team.lead.name)
    return render_template('crm/sales_teams.html', title=_('CRM Sales Teams | Olam ERP'), sales_teams=sales_teams)


@bp.route('/sales_team/<token>', methods=['GET', 'POST'])
@login_required
def sales_team(token):
    sales_team = Team.query.filter_by(token=token).join(Partner).first()
    return render_template('crm/sales_team.html', title=_(sales_team.name + ' | Olam ERP'), sales_team=sales_team)


@bp.route('/create_team', methods=['GET', 'POST'])
@login_required
def create_team():
    form = CreateSalesTeamForm()
    partners = Partner.query.filter_by(is_tenant=True).all()
    if form.validate_on_submit():
        sales_team = Team(name=form.name.data,
                          leader=request.form['team_leader'])
        sales_team.set_token(form.name.data)
        db.session.add(sales_team)
        db.session.commit()
        return redirect(url_for('crm.sales_teams'))
    return render_template('crm/create_team.html', title=_('CRM Sales Teams | Olam ERP'), form=form, partners=partners)


@bp.route('/reporting', methods=['GET', 'POST'])
@login_required
def reporting():
    pass


@bp.route('/configuration', methods=['GET', 'POST'])
@login_required
def configuration():
    pass


@bp.route('/lead/<slug>', methods=['GET', 'POST'])
def lead(slug):
    edit = False
    lead = Lead.query.filter_by(slug=slug).first()
    return render_template("crm/opportunity.html", title=_(lead.name + ' | Olam ERP'), lead=lead, slug=slug, edit=edit)


@bp.route('/edit/lead/<slug>', methods=['GET', 'POST'])
def edit_lead(slug):
    edit = True
    lead = Lead.query.filter_by(slug=slug).first()
    return render_template("crm/opportunity.html", title=_(lead.name + ' | Olam ERP'), lead=lead, edit=edit, slug=slug)


@bp.route('/move_stage/<slug>/<stage_id>', methods=['GET', 'POST'])
def move_stage(slug, stage_id):
    lead = Lead.query.filter_by(slug=slug).first()
    lead.stage_id = stage_id
    db.session.commit()
    return redirect(url_for('crm.pipeline'))
