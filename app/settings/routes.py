from flask.json import jsonify
from sqlalchemy import log
from app import db
from app.auth.email import send_invite_email
from app.main.models.partner import Partner
from app.settings import bp
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, session
from app.settings.forms import InviteForm
from flask_babel import _, lazy_gettext as _l
from app.auth.models.user import Users, Group


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


@bp.route('/groups', methods=['GET', 'POST'])
@login_required
def manage_groups():
    groups = Group.query.all()
    return render_template("settings/groups.html", title=_('Groups | Olam ERP'), groups=groups)


@bp.route('/new_group', methods=['GET', 'POST'])
@login_required
def new_group():
    group = None
    return render_template("settings/new_group.html", title=_('New Group | Olam ERP'), group=group)


@bp.route('/new_group/<slug>', methods=['GET', 'POST'])
@login_required
def newgroup(slug):
    group = Group.query.filter_by(slug=slug).join(Group.users).all()
    selected_users = Users.query.join(Users.groups).filter_by(slug=slug)
    return render_template("settings/new_group.html", group=group, title=_('New Group | Olam ERP'), selected_users=selected_users, slug=slug)


@bp.route('/select_users', methods=['GET', 'POST'])
@login_required
def select_users():
    if request.method == "POST":
        if "slug" in request.form:
            group = Group.query.filter_by(slug=request.form['slug']).first()
        else:
            group = Group()
            group.generate_slug()
            db.session.add(group)
            db.session.commit()
        session['selected_users'] = request.form['selected_user[]']
        for select_user in session['selected_users']:
            user = Users.query.filter_by(id=int(select_user)).first()
            group.users.append(user)
            db.session.commit()
    return jsonify({"response": "success", "slug": group.slug})


@bp.route('/discard/<slug>', methods=['GET', 'POST'])
@login_required
def discard_group(slug):
    group = Group.query.filter_by(slug=slug).first()
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('settings.manage_groups'))


@bp.route('/remove_user/<slug>/<id>', methods=['GET', 'POST'])
@login_required
def remove_user(slug, id):
    group = Group.query.filter_by(slug=slug).first()
    user = Users.query.filter_by(id=id).first()
    group.users.remove(user)
    db.session.commit()
    return redirect(url_for('settings.newgroup', slug=slug))
