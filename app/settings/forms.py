from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from flask_babel import _, lazy_gettext as _l
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app.main.models.partner import Partner


class InviteForm(FlaskForm):
    email = StringField(_l('Email Address'),
                        validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Invite'))

    def validate_email(self, email):
        partner = Partner.query.filter_by(email=email.data).first()
        if partner is not None:
            raise ValidationError(
                _('You can not have two users with the same email address!.'))


class NewGroup(FlaskForm):
    pass
