from app.auth.email import send_database_activation_email
import re
import time
from os import fsync
from app.main.models.database import Database
from app.main.models.company import Company
from app.auth.models.user import User
from app.main.utils import search_dict, updating
from app.main.models.module import Module, ModuleCategory
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, session, request, abort
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db, call_ansible
from app.main import bp
from app.main.forms import GetStartedForm
from config import basedir
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title=_('Tools to Grow Your Business | Olam ERP'))


@ bp.route('/dashboard')
@ login_required
def dashboard():
    return render_template('main/dashboard.html', title=_('Dashboard | Olam ERP'))


@ bp.route('/all-apps', methods=['GET', 'POST'])
@ login_required
def all_apps():
    return render_template('main/apps.html', title=_('All Apps | Olam ERP'))


@ bp.route('/home', methods=['GET', 'POST'])
# @login_required
def home():

    return render_template('main/home.html', title=_('Home | Olam ERP'))
