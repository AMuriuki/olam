from crypt import methods
import json
from app.helper_functions import set_default_user_groups
from app.main.models.partner import Partner
import os
from app.auth.email import send_database_activation_email, send_invite_email
import re
import time
from os import fsync
from app.main.models.database import Database
from app.main.models.company import Company
from app.auth.models.user import Group, Users, user_group
from app.main.models.product import Product
from app.main.models.uom import Uom
from app.main.utils import search_dict, updating
from app.main.models.module import Module
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, session, request, abort, Response
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
from app.decorators import active_user_required, model_access_required, module_access_required
from sqlalchemy.sql.elements import or_


@bp.route('/', methods=['GET', 'POST'])
@login_required
@active_user_required
def home():
    return redirect(url_for('main.index'))


@bp.route('/home', methods=['GET', 'POST'])
@login_required
@active_user_required
def index():
    return render_template('main/index.html', title=_('My Apps | Olam ERP'))


@bp.route('/dashboard')
@login_required
@active_user_required
def dashboard():
    return render_template('main/dashboard.html', title=_('Dashboard | Olam ERP'))


@bp.route('/all-apps', methods=['GET', 'POST'])
@login_required
@active_user_required
def all_apps():
    return render_template('main/apps.html', title=_('All Apps | Olam ERP'))


@bp.route('/invite_colleagues', methods=['GET', 'POST'])
@login_required
@active_user_required
def invite_colleagues():
    form = InviteForm()
    user = Users.query.filter_by(id=current_user.get_id()).first()
    invited_by = Partner.query.filter_by(id=user.partner_id).first()
    if form.validate_on_submit():
        if form.data['user1name'] and form.data['user1email']:
            partner = Partner(name=form.data['user1name'],
                              email=form.data['user1email'], company_id=current_user.company_id, is_tenant=True)
            partner.generate_slug()
            db.session.add(partner)
            db.session.commit()
            user = Users(partner_id=partner.id)
            user.generate_slug()
            db.session.add(user)
            db.session.commit()
            set_default_user_groups(user)
            send_invite_email(partner.id, invited_by.id)
        if form.data['user2name'] and form.data['user2email']:
            partner = Partner(name=form.data['user2name'],
                              email=form.data['user2email'], company_id=current_user.company_id, is_tenant=True)
            partner.generate_slug()
            db.session.add(partner)
            db.session.commit()
            user = Users(partner_id=partner.id)
            user.generate_slug()
            db.session.add(user)
            db.session.commit()
            set_default_user_groups(user)
            send_invite_email(partner.id, invited_by.id)
        if form.data['user3name'] and form.data['user3email']:
            partner = Partner(name=form.data['user3name'],
                              email=form.data['user3email'], company_id=current_user.company_id, is_tenant=True)
            partner.generate_slug()
            db.session.add(partner)
            db.session.commit()
            user = Users(partner_id=partner.id)
            user.generate_slug()
            db.session.add(user)
            db.session.commit()
            set_default_user_groups(user)
            send_invite_email(partner.id, invited_by.id)
        return redirect(url_for('main.index'))
    return render_template('main/invite_colleagues.html', title=_('Invite Colleagues | Olam ERP'), form=form)


@bp.route('/get_product_purchase_details', methods=['GET', 'POST'])
@login_required
@active_user_required
@module_access_required(5)
@model_access_required(9)
def get_product_purchase_details():
    if request.method == "POST":
        product = Product.query.filter_by(id=request.form['product']).first()
        return jsonify({'name': product.name, 'description': product.description, 'id': product.id, 'unit_price': product.price})


@bp.route('/get_products', methods=['GET', 'POST'])
@login_required
@active_user_required
@module_access_required(5)
@model_access_required(9)
def get_items():
    products = []
    results = Product.query.all()
    for result in results:
        manufacturer = result.manufacturer.name if result.manufacturer else None
        category = result.category.name if result.category else None
        name = result.name
        products.append({str(result.id): name})
    return Response(json.dumps(products), mimetype='application/json')


@bp.route('/get_UOM', methods=['GET', 'POST'])
@login_required
@active_user_required
@module_access_required(5)
@model_access_required(10)
def get_uom():
    uoms = []
    results = Uom.query.all()
    for result in results:
        uoms.append({str(result.id): result.name})
    return Response(json.dumps(uoms), mimetype='application/json')


@bp.route('/get_partners', methods=['GET', 'POST'])
@login_required
@active_user_required
@model_access_required(3)
def get_partners():
    partners = []
    results = db.session.query(Partner).filter(or_(
        Partner.is_company == True, Partner.is_individual == True)).all()
    for result in results:
        partners.append({str(result.id): result.get_name()})
    return Response(json.dumps(partners), mimetype='application/json')
