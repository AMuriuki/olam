from app.main.models.partner import Partner
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_babel import _, lazy_gettext as _l


def get_companies():
    return Partner.query.filter_by(is_company=True)


TITLES = ['Doctor', 'Engineer', 'Madam', 'Ms.', 'Mr.', 'Professor', 'Sir']


class BasicCompanyInfoForm(FlaskForm):
    companyname = StringField(_l('Company Name'))
    phonenumber = StringField(_l('Phone Number'))
    email = StringField(_l('Email Address'))
    website = StringField(_l('Website'))
    submit1 = SubmitField(_l('Save'))


class BasicIndividualInfoForm(FlaskForm):
    name = StringField(_l('Name'))
    phonenumber = StringField(_l('Phone Number'))
    email = StringField(_l('Email Address'))
    website = StringField(_l('Website'))
    jobposition = StringField(_l('Job Position'))
    submit2 = SubmitField(_l('Save'))


class AddressInfoForm(FlaskForm):
    postalcode = StringField(_l('Postal/Zip Code'))
    postaladdress = StringField(_l('Postal Address'))
    submit3 = SubmitField(_l('Save'))


class TaxInfoForm(FlaskForm):
    taxid = StringField(_l('Tax ID'))
    submit4 = SubmitField(_l('Save'))
