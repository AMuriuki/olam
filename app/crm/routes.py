from genericpath import exists
from select import select
from flask_login import login_required, current_user
from flask import json, render_template, session, jsonify, request, redirect, url_for, flash
from app.crm import bp
from app.crm.models.crm_lead import FILTERS, Lead, LeadActivity
from app.crm.models.crm_recurring_plan import RecurringPlan
from app.crm.models.crm_stage import Stage
from app.decorators import active_user_required, can_create_access_required, model_access_required, module_access_required
from app.main.models.activities import Activity
from app.main.models.module import Model, Module
from flask_babel import _, get_locale
from app import create_app, db
from app.main.models.partner import Partner, PartnerTeam
from sqlalchemy import log, or_
from app.contacts.forms import TITLES, BasicCompanyInfoForm, BasicIndividualInfoForm
from app.crm.forms import AddStage, BoardItemForm, NewRecurringPlanForm, EditStageForm, CreateSalesTeamForm
from flask_wtf.csrf import CSRFProtect

app = create_app()


@bp.route('/edit_stage', methods=['GET', 'POST'])
@login_required
@active_user_required
@module_access_required(2)
def edit_stage():
    stage = Stage.query.filter_by(id=request.form['stage_id']).first()
    stage.name = request.form['stage_name']
    db.session.commit()
    return jsonify({"response": "success"})


@login_required
@active_user_required
@bp.route('/delete_stage', methods=['GET', 'POST'])
def delete_stage():
    stage = Stage.query.filter_by(id=request.form['stage_id']).first()
    stage.is_deleted = True
    db.session.commit()
    return jsonify({"response": "success"})


@login_required
@active_user_required
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
@active_user_required
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
@active_user_required
@bp.route('/update_item', methods=['GET', 'POST'])
def update_item():
    opportunity = Lead.query.filter_by(id=request.form['item_id']).first()
    opportunity.priority = request.form['priority']
    db.session.commit()
    return jsonify({"response": "success"})


@login_required
@active_user_required
@bp.route('/get_partner_details', methods=['GET', 'POST'])
def get_partner_details():
    partner = Partner.query.filter_by(id=request.form['partner_id']).first()
    return jsonify({"partner_email": partner.email, "partner_phone": partner.phone_no})


@login_required
@active_user_required
@bp.route('/selected_priority', methods=['GET', 'POST'])
def select_priority():
    session['selected_priority'] = request.form['selected_priority']
    return jsonify({"response": "success"})


@login_required
@active_user_required
@bp.route('/pipeline_stage', methods=['GET', 'POST'])
def pipeline_stage():
    session['pipeline_stage'] = request.form['pipeline_stage']
    return jsonify({"response": "success"})


@login_required
@active_user_required
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
@active_user_required
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
@active_user_required
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


@bp.route('/get_opportunityID', methods=['POST', 'GET'])
def get_opportunityID():
    if request.method == "POST":
        session['opportunity_id'] = request.form['opportunity_id']
        return jsonify({"response": "success"})


@bp.route('/update-activity/<int:id>', methods=['POST', 'GET'])
def update_activity(activity_id):
    activity = Activity.query.filter_by(id=activity_id).first()
    module = Module.query.filter_by(bp_name='crm').first()
    model = Model.query.filter_by(name='Lead/Opportunity').first()
    if request.method == "POST":
        activity.summary = request.form['summary']
        activity.module_id = module.id
        activity.model_id = model.id
        activity.lead_id = session['opportunity_id']
        activity.activity_type = request.form['activity_type']
        activity.due_date = request.form['due_date']
        activity.assigned_to = request.form['assignee']
        activity.notes = request.form['notes']
        db.session.commit()
        flash(_("New activity added"))
        return redirect(url_for('crm.pipeline'))


@bp.route('/', methods=['GET', 'POST'])
@login_required
@active_user_required
@module_access_required(2)
def pipeline():
    form1 = BasicCompanyInfoForm()
    form2 = BasicIndividualInfoForm()
    form3 = BoardItemForm()
    form4 = NewRecurringPlanForm()
    form5 = EditStageForm()
    form6 = AddStage()
    csrf_token = CSRFProtect(app)
    plans = RecurringPlan.query.all()
    titles = TITLES

    filters = FILTERS
    new_stage = False
    message = None
    exists = []

    selectedFilters = request.args.get('filter')

    qs = Lead.query.order_by(Lead.priority.desc())

    if selectedFilters:
        _selectedFilters = selectedFilters.split(',')
        if "All" in selectedFilters:
            qs = qs
        else:
            if "My Pipeline" in selectedFilters:
                qs = qs.filter_by(user_id=current_user.get_id())
            if "Unassigned" in selectedFilters:
                qs = qs.filter_by(user_id=None)
                if qs.count() == 0:
                    message = "There are no unassigned opportunities"
                    flash(_("No unassigned opportunities"))
            for _filter in _selectedFilters:
                stage = Stage.query.filter_by(name=_filter).first()
                if stage:
                    exists.append(stage.id)
            if exists:
                print(exists)
                qs = qs.filter(Lead.stage_id.in_(exists))
        pipeline = qs.all()
    else:
        pipeline = Lead.query.filter_by(
            user_id=current_user.get_id()).order_by(Lead.priority.desc()).all()
        selectedFilters = "My Pipeline,"

    activities = LeadActivity.query.all()
    assignees = Partner.query.filter_by(is_tenant=True).all()

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

    if request.method == "POST":
        module = Module.query.filter_by(bp_name='crm').first()
        model = Model.query.filter_by(name='Lead/Opportunity').first()
        activity = Activity(summary=request.form['summary'], module_id=module.id, model_id=model.id, lead_id=session['opportunity_id'],
                            activity_type=request.form['activity_type'], due_date=request.form['due_date'], assigned_to=request.form['assignee'], notes=request.form['notes'])
        db.session.add(activity)
        db.session.commit()
        flash(_("New activity added"))
        return redirect(url_for('crm.pipeline'))

    return render_template('crm/pipeline.html', title=_('CRM Pipeline | Olam ERP'), pipeline=pipeline, form1=form1, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, titles=titles, plans=plans, filters=filters, new_stage=new_stage, selectedFilters=selectedFilters, message=message, activities=activities, assignees=assignees, csrf_token=csrf_token)


@bp.route('/pipeline', methods=['GET', 'POST'])
@login_required
@active_user_required
def empty():
    return render_template('crm/pipeline.html', title=_('CRM Pipeline | Olam ERP'))


@bp.route('/sales', methods=['GET', 'POST'])
@login_required
@active_user_required
def sales():
    pass


@bp.route('/sales_team', methods=['GET', 'POST'])
@login_required
@active_user_required
def sales_teams():
    sales_teams = PartnerTeam.query.join(Partner).all()
    for sales_team in sales_teams:
        print(sales_team.lead.name)
    return render_template('crm/sales_teams.html', title=_('CRM Sales Teams | Olam ERP'), sales_teams=sales_teams)


@bp.route('/sales_team/<token>', methods=['GET', 'POST'])
@login_required
@active_user_required
def sales_team(token):
    sales_team = PartnerTeam.query.filter_by(token=token).join(Partner).first()
    return render_template('crm/sales_team.html', title=_(sales_team.name + ' | Olam ERP'), sales_team=sales_team)


@bp.route('/create_team', methods=['GET', 'POST'])
@login_required
@active_user_required
def create_team():
    form = CreateSalesTeamForm()
    partners = Partner.query.filter_by(is_tenant=True).all()
    if form.validate_on_submit():
        sales_team = PartnerTeam(name=form.name.data,
                                 leader=request.form['team_leader'])
        sales_team.set_token(form.name.data)
        db.session.add(sales_team)
        db.session.commit()
        return redirect(url_for('crm.sales_teams'))
    return render_template('crm/create_team.html', title=_('CRM Sales Teams | Olam ERP'), form=form, partners=partners)


@bp.route('/reporting', methods=['GET', 'POST'])
@login_required
@active_user_required
def reporting():
    pass


@bp.route('/configuration', methods=['GET', 'POST'])
@login_required
@active_user_required
def configuration():
    pass


@login_required
@active_user_required
@bp.route('/lead/<slug>', methods=['GET', 'POST'])
def lead(slug):
    edit = False
    lead = Lead.query.filter_by(slug=slug).first()
    return render_template("crm/opportunity.html", title=_(lead.name + ' | Olam ERP'), lead=lead, slug=slug, edit=edit)


@login_required
@active_user_required
@bp.route('/edit/lead/<slug>', methods=['GET', 'POST'])
def edit_lead(slug):
    edit = True
    lead = Lead.query.filter_by(slug=slug).first()
    return render_template("crm/opportunity.html", title=_(lead.name + ' | Olam ERP'), lead=lead, edit=edit, slug=slug)


@login_required
@active_user_required
@bp.route('/move_stage/<slug>/<stage_id>', methods=['GET', 'POST'])
def move_stage(slug, stage_id):
    lead = Lead.query.filter_by(slug=slug).first()
    lead.stage_id = stage_id
    db.session.commit()
    return redirect(url_for('crm.pipeline'))


@bp.route('/activities', methods=['GET', 'POST'])
@login_required
@module_access_required(2)
@model_access_required(7)
@active_user_required
def activities():
    csrf_token = CSRFProtect(app)
    model_name = request.args.get('model')
    if model_name:
        model = Model.query.filter_by(name=model_name).first()
        activities = Activity.query.filter_by(model_id=model.id).all()
    else:
        activities = ""
    return render_template("crm/activities.html", title=_("Activities | Olam ERP"), activities=activities, csrf_token=csrf_token)


@bp.route('/create-activity', methods=['GET', 'POST'])
@login_required
@module_access_required(2)
@can_create_access_required(7)
@active_user_required
def create_activity():
    customers = db.session.query(Partner).filter(
        Partner.is_tenant == False).all()
    sales_people = Partner.query.filter_by(is_tenant=True).all()
    sales_teams = PartnerTeam.query.filter_by().all()
    if request.method == "POST":
        print(request.form['notes'])
    return render_template("crm/create_activity.html", title=_("New Activity | Olam ERP"), customers=customers, sales_people=sales_people, sales_teams=sales_teams)
