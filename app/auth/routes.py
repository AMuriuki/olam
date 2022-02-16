from datetime import datetime
import uuid
from app.main.models.partner import Partner
from app.main.models.module import Model, Module, ModuleCategory
from app.main.models.database import Database
from app.main.models.company import Company
from app.auth.models.user import Access, Group
from flask import render_template, redirect, url_for, flash, request, session, abort
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db, current_app, get_api_token, get_installed_modules_api, api_base
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm, SetPasswordForm
from app.auth.models.user import Users
from app.auth.email import send_password_reset_email
from sqlalchemy import or_
import requests
import json
from werkzeug.security import generate_password_hash, check_password_hash


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        partner = Partner.query.filter_by(
            email=form.email.data).first()
        if partner:
            user = Users.query.filter_by(partner_id=partner.id).first()

            if not user.password_hash:
                flash(
                    _('Your account is not active. Activate by setting a new password'))
                return redirect(url_for('auth.set_password', email=partner.email))
            if user is None or not user.check_password(form.password.data):
                flash(_('Invalid email or password'))
                return redirect(url_for('auth.login'))
            login_user(user)
            user.last_seen = datetime.utcnow()
            db.session.commit()
        else:
            flash(_('User does not exist'))
            return redirect(url_for('auth.login'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In | Olam ERP'), form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.args.get('token'):
        user = Users.verify_token(request.args.get('token'))
        partner = Partner.query.filter_by(id=user.partner_id).first()
        form.email.data = partner.email
        form.email.render_kw = {'disabled': 'disabled'}
        if form.validate_on_submit():
            partner.name = form.name.data
            partner.company_id = request.args.get('company')
            partner.is_tenant = True
            user.set_password(form.password.data)
            user.is_active = True
            user.company_id = request.args.get('company')
            db.session.commit()
            login_user(user)
            flash(_('Welcome to Olam ERP!'))
            return redirect(url_for('main.index'))
    else:
        if form.validate_on_submit():
            partner = Partner(name=form.name.data, email=form.email.data)
            partner.generate_slug()
            db.session.add(partner)
            db.session.commit()
            user = Users(partner_id=partner.id)
            user.set_password(form.password.data)
            user.set_token(partner.id)
            user.generate_slug()
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(_('Welcome to Olam ERP!'))
            return redirect(url_for('main.index'))
    return render_template('auth/register.html', title=_('Register | Olam ERP'),
                           form=form)


@bp.route('/set_password', methods=['GET', 'POST'])
def set_password():
    if request.args.get('domainname'):
        company = Company.query.filter_by(
            domain_name=request.args.get('domainname')).first()

        if company is None:
            company = Company(name=request.args.get('companyname'),
                              domain_name=request.args.get('domainname'))
            db.session.add(company)
            db.session.commit()

    if request.args.get('email'):
        partner = Partner.query.filter_by(
            email=request.args.get('email')).first()

        if partner is None:
            # first user registration
            partner = Partner(name=request.args.get('username'),
                              email=request.args.get('email'), phone_no=request.args.get('phone_no'), is_active=True, company_id=company.id, is_tenant=True)
            partner.generate_slug()
            db.session.add(partner)
            db.session.commit()
            user = Users(partner_id=partner.id, company_id=company.id,
                         is_active=True, country_code=request.args.get('country_code'))
            user.set_token(partner.id)
            user.generate_slug()
            db.session.add(user)
            db.session.commit()
        else:
            # existing user
            user = Users.query.filter_by(partner_id=partner.id).first()

    form = SetPasswordForm()
    if user:
        if user.password_hash:
            return redirect(url_for('main.index'))
        else:
            if form.validate_on_submit():
                user.password_hash = generate_password_hash(form.password.data)
                user.is_active = True
                db.session.commit()
                login_user(user)
                exists = Module.query.first()
                if exists:
                    # modules/DB already set-up
                    return redirect(url_for('main.index'))
                else:
                    # first time modules/DB set up
                    company_id = request.args.get('companyid')
                    link = get_installed_modules_api + \
                        str(company_id) + '/modules'
                    get_installed_modules(link)
                    get_access_groups()
                    get_access_rights()
                    set_admin_groups()
                    return redirect(url_for('main.invite_colleagues'))
    return render_template('auth/set_password.html', title=_('Set Password | Olam ERP'), form=form)


def set_admin_groups():
    groups = Group.query.filter_by(permission=3).all()
    for group in groups:
        group.users.append(current_user)
        db.session.commit()


def get_installed_modules(link):
    response = requests.get(link)
    response_dict = json.loads(response.content)
    for i in range(len(response_dict['items'])):
        module_category = ModuleCategory.query.filter_by(
            id=response_dict['items'][i]['category_id']).first()
        if not module_category:
            module_category = ModuleCategory(
                id=response_dict['items'][i]['category_id'], name=response_dict['items'][i]['category_name'])
            db.session.add(module_category)
            db.session.commit()
        module = Module(id=response_dict['items'][i]['id'], technical_name=response_dict['items'][i]['technical_name'], official_name=response_dict['items']
                        [i]['official_name'], bp_name=response_dict['items'][i]['bp_name'], summary=response_dict['items'][i]['summary'], category_id=response_dict['items'][i]['category_id'], user_groups_api=response_dict['items'][i]['links']['access_groups'], models_api=response_dict['items'][i]['links']['models'])
        db.session.add(module)
        db.session.commit()


def get_access_groups():
    modules = Module.query.all()
    for module in modules:
        response = requests.get(api_base+module.user_groups_api)
        response_dict = json.loads(response.content)
        for i in range(len(response_dict['items'])):
            exists = Group.query.filter_by(
                id=response_dict['items'][i]['id']).first()
            if not exists:
                group = Group(id=response_dict['items'][i]['id'], name=response_dict['items'][i]['name'],
                              module_id=response_dict['items'][i]['module_id'], permission=response_dict['items'][i]['permission'], access_rights_url=response_dict['items'][i]['links']['access_rights'])
                group.generate_slug()
                db.session.add(group)
                db.session.commit()


def get_models():
    modules = Module.query.all()
    for module in modules:
        response = requests.get(api_base+module.models_api)
        response_dict = json.loads(response.content)
        for i in range(len(response_dict['items'])):
            exists = Model.query.filter_by(id=model['id']).first()
        if not exists:
            model = Model(id=model['id'], name=model['name'],
                          description=model['description'])
            model.generate_slug()
            db.session.add(model)
            db.session.commit()


def get_access_rights():
    groups = Group.query.all()
    for group in groups:
        response = requests.get(api_base + group.access_rights_url)
        response_dict = json.loads(response.content)
        for i in range(len(response_dict['items'])):
            exists = Access.query.filter_by(
                id=response_dict['items'][i]['id']).first()
            if not exists:
                access = Access(id=response_dict['items'][i]['id'], name=response_dict['items'][i]['name'], model_id=response_dict['items'][i]['model_id'], read=response_dict['items']
                                [i]['read'], write=response_dict['items'][i]['write'], create=response_dict['items'][i]['create'], delete=response_dict['items'][i]['delete'])
                db.session.add(access)
                db.session.commit()
                group.rights.append(access)
            db.session.commit()


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password | Olam ERP'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = Users.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('/activate/<token>', methods=['GET', 'POST'])
def activate(token):
    form = SetPasswordForm()
    user = Users.verify_token(token)
    partner = Partner.query.filter_by(id=user.partner_id).first()
    if not partner.name:
        return redirect(url_for('auth.register', token=token, company=request.args.get('company')))
    if not user:
        abort(401)
    else:
        if form.validate_on_submit():
            user.password_hash = generate_password_hash(form.password.data)
            user.is_active = True
            user.company_id = request.args.get('company')
            db.session.commit()
            login_user(user)
            user.last_seen = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('auth/set_password.html', title=_('Set Password | Olam ERP'), form=form, var='Account')
