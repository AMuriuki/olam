from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.auth.models.user import Users
from app.main.models.partner import Partner


class LoginForm(FlaskForm):
    email = StringField(_l('Email'),
                        validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    email = StringField(_l('Your Email Address'),
                        validators=[DataRequired(), Email()])
    name = StringField(_l('Your Name'),
                       validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Confirm Password'), validators=[DataRequired(),
                                            EqualTo('password')])
    submit = SubmitField(_l('Register'))

    # def validate_email(self, email):
    #     partner = Partner.query.filter_by(email=email.data).first()
    #     if partner is not None:
    #         raise ValidationError(
    #             _('There\'s an account with this email. Use a different one.'))


class SetPasswordForm(FlaskForm):
    password = PasswordField('Choose a password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm your password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Activate')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
