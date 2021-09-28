from app.main.models.module import Module
from flask_login import login_required
from sqlalchemy import log
from app import contacts
from app.contacts import bp
from app.main.models.partner import Partner
from flask import render_template
from flask_babel import _, get_locale


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    contacts = Partner.query.all()
    return render_template('contacts/index.html', title=_('Contacts | Olam ERP'), contacts=contacts)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    return render_template('contacts/create.html', title=_('New Contact | Olam ERP'))
