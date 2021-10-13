from app.main.models.partner import Partner
from app.main.models.company import Company
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length, Email, Regexp
from flask_babel import _, lazy_gettext as _l



class GetStartedForm(FlaskForm):
    name = StringField(_l('Name'),
                       validators=[DataRequired()])
    email = StringField(_l('Email'),
                        validators=[DataRequired(), Email()])
    phonenumber = StringField(_l('Phone Number'),
                              validators=[DataRequired()])
    companyname = StringField(_l('Company Name'),
                              validators=[DataRequired()])
    domainoutput = StringField(_l('Domain'),
                               validators=[DataRequired(), Regexp(r'^[\w.@+-]+$', message="Spaces are not allowed in domain names")], render_kw={'readonly': True})
    submit = SubmitField(_l('Start Now'))


class InviteForm(FlaskForm):
    user1name = StringField(_l('Name'))
    user2name = StringField(_l('Name'))
    user3name = StringField(_l('Name'))
    user1email = StringField(_l('Email'))
    user2email = StringField(_l('Email'))
    user3email = StringField(_l('Email'))
    submit = SubmitField(_('Send Invites'))
