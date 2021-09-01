import os
from flask import render_template, current_app
from flask_babel import _
from sendgrid.helpers.mail import Mail
from sendgrid.sendgrid import SendGridAPIClient
from app.sendgrid_email import send_email


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[Olam-ERP] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_database_activation_email(user, domain_name):
    token = user.get_database_activation_token()
    message = Mail(from_email=current_app.config['ADMINS'][0], to_emails=[user.email], subject='Activate ' + domain_name +
                   '.olam-erp.com', html_content=render_template('email/activate_database.html', user=user, token=token, domain_name=domain_name))
    send_email(message)
