from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.api.errors import error_response
from app.auth.models.user import Users
from app.main.models.partner import Partner

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    partner = Partner.query.filter_by(email=username).first()
    user = Users.query.filter_by(partner_id=partner.id).first()
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    return Users.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)
