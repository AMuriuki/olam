from app.main.models.partner import Partner
from app.main.models.module import Module
from app.main.models.database import Database
from app.main.models.company import Company
from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db, current_app, get_api_token, get_installed_modules
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm, SetPasswordForm
from app.auth.models.user import User
from app.auth.email import send_password_reset_email
from sqlalchemy import or_
import requests
import json
from app.auth.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

from app.tasks import ManageTasks


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        partner = Partner.query.filter_by(
            email=form.email.data).first()
        user = User.query.filter_by(partner_id=partner.id).first()
        if user is None or not user.check_password(form.password.data):

            flash(_('Invalid email or password'))
            return redirect(url_for('auth.login'))

        login_user(user)
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
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, role_id=3)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(_('Welcome to Olam ERP!'))
        return redirect(url_for('main.getting_started'))
    return render_template('auth/register.html', title=_('Register | Olam ERP'),
                           form=form)


@bp.route('/set_password', methods=['GET', 'POST'])
def set_password():
    partner = Partner.query.filter_by(email=request.args.get('email')).first()
    company = Company.query.filter_by(
        domain_name=request.args.get('domainname')).first()

    if company is None:
        company = Company(name=request.args.get('companyname'),
                          domain_name=request.args.get('domainname'))
        db.session.add(company)
        db.session.commit()

    if partner is None:
        partner = Partner(name=request.args.get('username'),
                          email=request.args.get('email'), phone_no=request.args.get('phone_no'), is_active=True, company_id=company.id, is_tenant=True)
        db.session.add(partner)
        db.session.commit()
        user = User(partner_id=partner.id, company_id=company.id,
                    is_active=True, country_code=request.args.get('country_code'))
        db.session.add(user)
        db.session.commit()
    else:
        user = User.query.filter_by(partner_id=partner.id).first()

    response = requests.post(get_api_token, auth=(
        partner.email, 'api_user'))

    response_dict = json.loads(response.content)

    form = SetPasswordForm()
    if user.password_hash:
        return redirect(url_for('main.index'))
    else:
        if form.validate_on_submit():
            user.password_hash = generate_password_hash(form.password.data)
            db.session.commit()
            login_user(user)
            head = {'Authorization': 'Bearer ' + response_dict['token']}
            company_id = request.args.get('companyid')
            response = requests.get(
                get_installed_modules + str(company_id) + '/modules', headers=head)
            response_dict = json.loads(response.content)

            for i in range(len(response_dict['items'])):
                module = Module(technical_name=response_dict['items'][i]['technical_name'], official_name=response_dict['items'][i]['official_name'], bp_name=response_dict['items'][i]['bp_name'], summary=response_dict['items'][i]['summary'])
                db.session.add(module)
                db.session.commit()
            return redirect(url_for('main.invite_colleagues'))
    return render_template('auth/set_password.html', title=_('Set Password | Olam ERP'), form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
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
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
