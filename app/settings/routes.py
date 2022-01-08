from flask.json import jsonify
from sqlalchemy import log
from app import db
from app.auth.email import send_invite_email
from app.main.models.partner import Partner
from app.settings import bp
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for
from app.settings.forms import InviteForm
from flask_babel import _, lazy_gettext as _l
from app.auth.models.user import Users


@bp.route('/general_settings', methods=['GET', 'POST'])
@login_required
def general():
    form = InviteForm()
    pending_invitations = Users.query.filter_by(is_active=False).all()
    return render_template('settings/settings.html', title=_('General Settings | Olam ERP'), form=form, pending_invitations=pending_invitations)


@bp.route('/invite', methods=['GET', 'POST'])
@login_required
def invite():
    form = InviteForm()
    user = Users.query.filter_by(id=current_user.get_id()).first()
    invited_by = Partner.query.filter_by(id=user.partner_id).first()
    if form.validate_on_submit():
        partner = Partner(email=form.email.data)
        partner.generate_slug()
        db.session.add(partner)
        db.session.commit()
        user = Users(partner_id=partner.id)
        user.set_token(partner.id)
        db.session.add(user)
        db.session.commit()
        send_invite_email(partner.id, invited_by.id)
        return jsonify({'response': "success"})
    if form.errors:
        print(form.errors)
        return jsonify({'response': form.errors})


@bp.route('/user/<token>')
@login_required
def user(token):
    pass
