from app.decorators import active_user_required
from app.main.models.country import City, Country
from app.main.utils import get_countries, get_countries_cities
from flask import url_for, request, jsonify
from app.main.models.module import Module
from flask_login import login_required
from sqlalchemy import log
from app import contacts
from app.contacts import bp
from app.main.models.partner import Partner
from flask import render_template, redirect
from flask_babel import _, get_locale
from app.contacts.forms import BasicCompanyInfoForm, BasicIndividualInfoForm, TITLES, AddressInfoForm, TaxInfoForm
from app import db


@bp.route('/', methods=['GET', 'POST'])
@login_required
@active_user_required
def index():
    contacts = Partner.query.all()
    return render_template('contacts/index.html', title=_('Contacts | Olam ERP'), contacts=contacts)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
@active_user_required
def create():
    form1 = BasicCompanyInfoForm()
    form2 = BasicIndividualInfoForm()

    titles = TITLES
    countries = Country.query.order_by('name').all()
    companies = Partner.query.filter_by(is_company=True).all()

    if "submit1" in request.form and form1.validate_on_submit():
        partner = Partner(company_name=form1.companyname.data, phone_no=form1.phonenumber.data, website=form1.website.data, is_company=True, is_active=True, email=form1.email.data,
                          country_id=request.form['select_country'], city_id=request.form['select_city'], postal_code=form1.postalcode.data, postal_address=form1.postaladdress.data, tax_id=form1.taxid.data)
        partner.generate_slug()
        db.session.add(partner)
        db.session.commit()
        return redirect(url_for('contacts.view_contact', slug=partner.slug))
    if "submit2" in request.form and form2.validate_on_submit():
        partner = Partner(name=form2.name.data,
                          phone_no=form2.phonenumber.data, title=request.form['select_title'], parent_id=request.form['individual_select_company'], website=form2.website.data, is_individual=True, is_active=True, function=form2.jobposition.data, email=form2.email.data)
        partner.generate_slug()
        db.session.add(partner)
        db.session.commit()
        return redirect(url_for('contacts.view_contact', slug=partner.slug))
    return render_template('contacts/create.html', title=_('New Contact | Olam ERP'), form1=form1, form2=form2, companies=companies, titles=titles, countries=countries)


@bp.route('/view_contact/<slug>', methods=['GET', 'POST'])
@login_required
@active_user_required
def view_contact(slug):
    form1 = BasicCompanyInfoForm()
    form2 = BasicIndividualInfoForm()
    form3 = AddressInfoForm()
    form4 = TaxInfoForm()
    partner = Partner.query.filter_by(slug=slug).first()
    titles = TITLES
    companies = Partner.query.filter_by(is_company=True).all()
    countries = Country.query.order_by('name').all()

    if "submit1" in request.form and form1.validate_on_submit():
        if partner.is_company:
            partner.company_name = form1.companyname.data
            partner.phone_no = form1.phonenumber.data
            partner.website = form1.website.data
            partner.email = form1.email.data
            db.session.commit()
            return redirect(url_for('contacts.view_contact', slug=partner.slug))
    if "submit2" in request.form and form2.validate_on_submit():
        if partner.is_individual or partner.is_tenant:
            partner.name = form2.name.data
            partner.title = request.form['select_title']
            partner.function = form2.jobposition.data
            partner.phone_no = form2.phonenumber.data
            partner.email = form2.email.data
            partner.website = form2.website.data
            db.session.commit()
            return redirect(url_for('contacts.view_contact', slug=partner.slug))
    if "submit3" in request.form and form3.validate_on_submit():
        partner.country_id = request.form['select_country']
        partner.city_id = request.form['select_city'] if request.form['select_city'].isdigit() else None
        partner.postal_code = form3.postalcode.data
        partner.postal_address = form3.postaladdress.data
        db.session.commit()
        return redirect(url_for('contacts.view_contact', slug=partner.slug))
    if "submit4" in request.form and form4.validate_on_submit():
        partner.tax_id = form4.taxid.data
        db.session.commit()
        return redirect(url_for('contacts.view_contact', slug=partner.slug))
    return render_template('contacts/view.html', title=_('Contact Details | Olam ERP'), partner=partner, form1=form1, form2=form2, form3=form3, form4=form4, titles=titles, companies=companies, countries=countries)


@bp.route('/get_cities', methods=['GET', 'POST'])
@login_required
@active_user_required
def get_city():
    if request.method == "POST":
        cities = City.to_collection_dict(
            City.query.filter_by(country_id=request.json['country']).order_by('name'))
        return jsonify({'cities': cities})


@bp.route('/address/<slug>', methods=['GET', 'POST'])
@login_required
@active_user_required
def addresses(slug):
    partner = Partner.query.filter_by(slug=slug).first()
    children = Partner.query.filter_by(parent_id=partner.id).all()
    return render_template('contacts/addresses.html', title=_(partner.company_name + ' | Olam ERP'), partner=partner, children=children)


@bp.route('/meetings/<slug>', methods=['GET', 'POST'])
@login_required
@active_user_required
def meetings(slug):
    partner = Partner.query.filter_by(slug=slug).first()
    return render_template('contacts/meetings.html', title=_('Meetings | Olam ERP'), partner=partner)
