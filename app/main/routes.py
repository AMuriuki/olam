from app.main.models.partner import Partner
import os
from app.auth.email import send_database_activation_email
import re
import time
from os import fsync
from app.main.models.database import Database
from app.main.models.company import Company
from app.auth.models.user import User
from app.main.utils import search_dict, updating
from app.main.models.module import Module
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, session, request, abort
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main import bp
from app.main.forms import GetStartedForm, InviteForm
from config import basedir
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():

    return render_template('main/index.html', title=_('My Apps | Olam ERP'))


@ bp.route('/dashboard')
@ login_required
def dashboard():
    return render_template('main/dashboard.html', title=_('Dashboard | Olam ERP'))


@ bp.route('/all-apps', methods=['GET', 'POST'])
@ login_required
def all_apps():
    return render_template('main/apps.html', title=_('All Apps | Olam ERP'))


@ bp.route('/invite_colleagues', methods=['GET', 'POST'])
@login_required
def invite_colleagues():
    form = InviteForm()
    if form.validate_on_submit():
        if form.data['user1name'] and form.data['user1email']:
            partner = Partner(name=form.data['user1name'],
                              email=form.data['user1email'], company_id=current_user.company_id, is_tenant=True)
            db.session.add(partner)
            db.session.commit()
            user = User(partner_id=partner.id)
            db.session.add(user)
            db.session.commit()
        if form.data['user2name'] and form.data['user2email']:
            partner = Partner(name=form.data['user2name'],
                              email=form.data['user2email'], company_id=current_user.company_id, is_tenant=True)
            db.session.add(partner)
            db.session.commit()
            user = User(partner_id=partner.id)
            db.session.add(user)
            db.session.commit()
        if form.data['user3name'] and form.data['user3email']:
            partner = Partner(name=form.data['user3name'],
                              email=form.data['user3email'], company_id=current_user.company_id, is_tenant=True)
            db.session.add(partner)
            db.session.commit()
            user = User(partner_id=partner.id)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/invite_colleagues.html', title=_('Invite Colleagues | Olam ERP'), form=form)
