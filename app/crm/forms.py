from wtforms.fields.core import SelectField
from app.main.models.partner import Partner
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class BoardItemForm(FlaskForm):
    opportunity = StringField(_l('Opportunity'))
    email = StringField(_l('Email Address'))
    website = StringField(_l('Website'))
    submit1 = SubmitField(_l('Save'))
