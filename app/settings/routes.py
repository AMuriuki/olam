from flask.json import jsonify
from itsdangerous import json
from sqlalchemy import log
from app import db
from app.auth.email import send_invite_email
from app.main.models.partner import Partner
from app.settings import bp
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, session, flash
from app.settings.forms import InviteForm, NewGroup
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
    form = NewGroup()
    group = None
    if form.validate_on_submit():
        exists = Group.query.filter_by(name=request.form['group_name']).first()
        if exists:
            flash(
                _('A group with this name exists. Provide a unique name for the group.'))
            return jsonify({"response": "group name exists!"})
        else:
            group = Group(
                name=request.form['group_name'], module_id=request.form['select_app'])
            group.generate_slug()
            db.session.add(group)
            db.session.commit()
            return jsonify({"response": "success", "slug": group.slug})
    return render_template("settings/new_group.html", title=_('New Group | Olam ERP'), group=group, form=form)


@bp.route('/new_group/<slug>', methods=['GET', 'POST'])
@login_required
def newgroup(slug):
    form = NewGroup()
    # group = Group.query.filter_by(slug=slug).join(Group.users).all()
    group = Group.query.filter_by(slug=slug).first()
    group_members = Users.query.join(Users.groups).filter_by(slug=slug)
    if form.validate_on_submit():
        exists = Group.query.filter_by(name=request.form['group_name']).first()
        if exists:
            flash(
                _('A group with this name exists. Provide a unique name for the group.'))
            return jsonify({"response": "group name exists!"})
        else:
            group.name = request.form['group_name']
            group.module_id = request.form['select_app']
            db.session.commit()
            return jsonify({"response": "success"})
    return render_template("settings/new_group.html", group=group, title=_('New Group | Olam ERP'), group_members=group_members, slug=slug, form=form)


@bp.route('/group/<slug>', methods=['GET', 'POST'])
def group(slug):
    group = Group.query.filter_by(slug=slug).first()
    group_members = Users.query.join(Users.groups).filter_by(slug=slug)
    if not group:
        return redirect(url_for('settings.new_group'))
    return render_template("settings/group.html", group=group, title=_(str(group.name) + ' | Olam ERP'), group_members=group_members, slug=group.slug)


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
        session['selected_users'] = request.form.getlist(
            'selected_users[]')
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


@bp.route('/delete-group', methods=['GET', 'POST'])
def delete_group():
    selected = request.form.getlist(
        'selected_grops[]')
    for group in selected:
        group = Group.query.filter_by(id=group).first()
        group.is_deleted = True
        db.session.commit()
        return jsonify({"response": "success"})


@bp.route('/remove_user', methods=['GET', 'POST'])
@login_required
def remove_user():
    if request.method == "POST":
        group = Group.query.filter_by(slug=request.form['slug']).first()
        user = Users.query.filter_by(id=request.form['user_id']).first()
        group.users.remove(user)
        db.session.commit()
        return jsonify({'response': 'success'})


@bp.route('/edit_group/<slug>', methods=['GET', 'POST'])
@login_required
def edit_group(slug):
    edit = True
    form = NewGroup()
    group = Group.query.filter_by(slug=slug).first()
    group_members = Users.query.join(Users.groups).filter_by(slug=slug)
    return render_template("settings/edit_group.html", group=group, title=_("Edit " + str(group.name) + " | Olam ERP"), form=form, group_members=group_members, slug=group.slug, edit=edit)
