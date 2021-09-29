from app.main.models.country import Country
from app.main.utils import get_countries, get_countries_cities
from flask import url_for, request
from app.main.models.module import Module
from flask_login import login_required
from sqlalchemy import log
from app import contacts
from app.contacts import bp
from app.main.models.partner import Partner
from flask import render_template, redirect
from flask_babel import _, get_locale
from app.contacts.forms import BasicCompanyInfoForm, BasicIndividualInfoForm, TITLES, AddressInfo
from app import db


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    contacts = Partner.query.all()
    return render_template('contacts/index.html', title=_('Contacts | Olam ERP'), contacts=contacts)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form1 = BasicCompanyInfoForm()
    form2 = BasicIndividualInfoForm()
    form3 = AddressInfo()
    titles = TITLES
    countries = Country.query.order_by('name').all()    
    companies = Partner.query.filter_by(is_company=True).all()
    if "submit1" in request.form and form1.validate_on_submit():
        partner = Partner(company_name=form1.companyname.data,
                          phone_no=form1.phonenumber.data, website=form1.website.data, is_company=True, is_active=True)
        db.session.add(partner)
        db.session.commit()
        return redirect(url_for('contacts.view_contact', id=partner.id))
    if "submit2" in request.form and form2.validate_on_submit():
        partner = Partner(name=form2.name.data,
                          phone_no=form2.phonenumber.data, title=request.form['select_title'], parent_id=request.form['select_company'], website=form2.website.data, is_individual=True, is_active=True, function=form2.jobposition.data, email=form2.email.data)
        db.session.add(partner)
        db.session.commit()
        return redirect(url_for('contacts.view_contact', id=partner.id))
    if "submit3" in request.form and form3.validate_on_submit():
        partner = Partner()
    return render_template('contacts/create.html', title=_('New Contact | Olam ERP'), form1=form1, form2=form2, companies=companies, titles=titles, countries=countries)


@bp.route('/view_contact/<int:id>', methods=['GET', 'POST'])
@login_required
def view_contact(id):
    form1 = BasicCompanyInfoForm()
    form2 = BasicIndividualInfoForm()
    partner = Partner.query.filter_by(id=id).first()
    titles = TITLES
    companies = Partner.query.filter_by(is_company=True).all()
    if form1.validate_on_submit():
        if partner.is_company:
            partner.company_name = form1.companyname.data
        partner.phone_no = form1.phonenumber.data
        partner.website = form1.website.data
        partner.email = form1.email.data
        db.session.commit()
    return render_template('contacts/view.html', title=_('Contact Details | Olam ERP'), partner=partner, form1=form1, form2=form2, titles=titles, companies=companies)
