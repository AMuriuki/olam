from flask.json import jsonify
from itsdangerous import json
from sqlalchemy import log
from app import db
from app.auth.email import send_invite_email
from app.main.models.partner import Partner
from app.models import Model
from app.settings import bp
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, session, flash
from app.settings.forms import InviteForm, NewGroup
from flask_babel import _, lazy_gettext as _l
from app.auth.models.user import Access, Users, Group


@bp.route("/get_models", methods=['GET', 'POST'])
def get_models():
    if request.method == "POST":
        models = Model.to_collection_dict(Model.query.order_by('name'))
        return jsonify(models)


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
        user.generate_slug()
        db.session.add(user)
        db.session.commit()
        send_invite_email(partner.id, invited_by.id)
        return jsonify({'response': "success"})
    if form.errors:
        print(form.errors)
        return jsonify({'response': form.errors})


@bp.route('/groups', methods=['GET', 'POST'])
@login_required
def manage_groups():
    groups = Group.query.filter_by(is_active=True).all()
    return render_template("settings/groups.html", title=_('Groups | Olam ERP'), groups=groups)


@bp.route('/new_group', methods=['GET', 'POST'])
@login_required
def new_group():
    form = NewGroup()
    group = None
    models = Model.query.order_by('name').all()
    if form.validate_on_submit():
        exists = Group.query.filter_by(
            name=request.form['group_name']).filter_by(is_active=True).first()
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
            flash(
                _('Your group has been created successfully.'))
            return jsonify({"response": "success", "slug": group.slug})
    return render_template("settings/new_group.html", title=_('New Group | Olam ERP'), group=group, form=form, models=models)


@ bp.route('/new_group/<slug>', methods=['GET', 'POST'])
@ login_required
def newgroup(slug):
    form = NewGroup()
    group = Group.query.filter_by(slug=slug).first()
    group_members = Users.query.join(Users.groups).filter_by(slug=slug)
    access_rights = Access.query.join(Access.groups).filter_by(slug=slug)
    models = Model.query.order_by('name').all()
    if form.validate_on_submit():
        exists = Group.query.filter_by(
            name=request.form['group_name']).filter_by(is_active=True).filter(Group.id != group.id).first()
        if exists:
            flash(
                _('A group with this name exists. Provide a unique name for the group.'))
            return jsonify({"response": "group name exists!"})
        else:
            group.name = request.form['group_name']
            group.module_id = request.form['select_app']
            db.session.commit()
            flash(
                _('This group has been saved successfully.'))
            return jsonify({"response": "success", "slug": group.slug})
    return render_template("settings/new_group.html", group=group, title=_('New Group | Olam ERP'), group_members=group_members, slug=slug, form=form, models=models, access_rights=access_rights)


@ bp.route("/settings/update/<slug>", methods=['GET', 'POST'])
def update_group(slug):
    form = NewGroup()
    group = Group.query.filter_by(slug=slug).first()
    if form.validate_on_submit():
        exists = Group.query.filter_by(
            name=request.form['group_name']).filter_by(is_active=True).filter(Group.id != group.id).first()
        if exists:
            flash(
                _('A group with this name exists. Provide a unique name for the group.'))
            return jsonify({"response": "group name exists!", "slug": slug})
        else:
            group.name = request.form['group_name']
            group.module_id = request.form['select_app']
            db.session.commit()
            return jsonify({"response": "success"})
    return redirect(url_for('settings.group', slug=slug))


@ bp.route('/group/<slug>', methods=['GET', 'POST'])
def group(slug):
    group = Group.query.filter_by(slug=slug).first()
    group_members = Users.query.join(Users.groups).filter_by(slug=slug)
    access_rights = Access.query.join(Access.groups).filter_by(slug=slug)
    models = Model.query.order_by('name').all()
    if not group:
        return redirect(url_for('settings.new_group'))
    return render_template("settings/group.html", group=group, title=_(str(group.name) + ' | Olam ERP'), group_members=group_members, slug=group.slug, access_rights=access_rights, models=models, page="group_members")


@ bp.route('/select_users', methods=['GET', 'POST'])
@ login_required
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


@ bp.route('/discard/<slug>', methods=['GET', 'POST'])
@ login_required
def discard_group(slug):
    group = Group.query.filter_by(slug=slug).first()
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('settings.manage_groups'))


@ bp.route('/delete-group', methods=['GET', 'POST'])
@ login_required
def delete_group():
    if request.method == "POST":
        selected = request.form.getlist(
            'selected_groups[]')
        for group in selected:
            group = Group.query.filter_by(id=group).first()
            group.is_active = False
            db.session.commit()
        return jsonify({"response": "success"})


@ bp.route('/remove_user', methods=['GET', 'POST'])
@ login_required
def remove_user():
    if request.method == "POST":
        group = Group.query.filter_by(slug=request.form['slug']).first()
        user = Users.query.filter_by(id=request.form['user_id']).first()
        group.users.remove(user)
        db.session.commit()
        return jsonify({'response': 'success'})


@ bp.route('/edit_group/<slug>', methods=['GET', 'POST'])
@ login_required
def edit_group(slug):
    edit = True
    form = NewGroup()
    group = Group.query.filter_by(slug=slug).first()
    group_members = Users.query.join(Users.groups).filter_by(slug=slug)
    access_rights = Access.query.join(Access.groups).filter_by(slug=slug)
    models = Model.query.order_by('name').all()
    return render_template("settings/edit_group.html", group=group, title=_("Edit " + str(group.name) + " | Olam ERP"), form=form, group_members=group_members, slug=group.slug, edit=edit, access_rights=access_rights, models=models)


@ bp.route('/access-right', methods=['GET', 'POST'])
def new_access_right():
    if request.method == "POST":
        if "access" in request.form:
            print(request.form)
            access = Access.query.filter_by(id=request.form['access']).first()
            if "name" in request.form:
                access.name = request.form['name']
                db.session.commit()
            if "model_id" in request.form:
                access.model_id = request.form['model_id']
                model_name = access.model.name
                db.session.commit()
            if "read" in request.form:
                if request.form['read'] == "true":
                    access.read = True
                else:
                    access.read = False
                db.session.commit()
            if "write" in request.form:
                if request.form['write'] == "true":
                    access.write = True
                else:
                    access.write = False
                db.session.commit()
            if "create" in request.form:
                if request.form['create'] == "true":
                    access.create = True
                else:
                    access.create = False
                db.session.commit()
            if "delete" in request.form:
                if request.form['delete'] == "true":
                    access.delete = True
                else:
                    access.delete = False
                db.session.commit()

            return jsonify({"response": "success", "model_name": model_name if model_name else None})
        else:
            exists = Access.query.filter_by(
                name=request.form['access_name']).first()
            if exists:
                return jsonify({"response": "access name exists"})
            else:
                if "read" in request.form:
                    if request.form['read'] == "true":
                        read = True
                    else:
                        read = False
                    db.session.commit()
                if "write" in request.form:
                    if request.form['write'] == "true":
                        write = True
                    else:
                        write = False
                    db.session.commit()
                if "create" in request.form:
                    if request.form['create'] == "true":
                        create = True
                    else:
                        create = False
                    db.session.commit()
                if "delete" in request.form:
                    if request.form['delete'] == "true":
                        delete = True
                    else:
                        delete = False
                    db.session.commit()
                group = Group.query.filter_by(
                    slug=request.form['group']).first()
                access = Access(
                    name=request.form['access_name'], model_id=request.form['model'], read=read, write=write, create=create, delete=delete)
                access.generate_slug()
                db.session.add(access)
                group.rights.append(access)
                db.session.commit()
                return jsonify({"response": "success", "access": access.id})


@ bp.route('/remove_access_right', methods=['GET', 'POST'])
@ login_required
def remove_access_right():
    if request.method == "POST":
        group = Group.query.filter_by(slug=request.form['group']).first()
        access_right = Access.query.filter_by(
            id=request.form['access']).first()
        group.rights.remove(access_right)
        Access.query.filter_by(id=request.form['access']).delete()
        db.session.commit()
        return jsonify({'response': 'success'})


@ bp.route('/group/members/<slug>', methods=['GET', 'POST'])
def group_members(slug):
    group = Group.query.filter_by(slug=slug).first()
    group_members = Users.query.join(Users.groups).filter_by(slug=slug)
    return render_template("settings/group.html", group=group, title=_(str(group.name) + ' | Olam ERP'), group_members=group_members, slug=group.slug, page="group_members")


@ bp.route('/group/rights/<slug>', methods=['GET', 'POST'])
def group_rights(slug):
    group = Group.query.filter_by(slug=slug).first()
    access_rights = Access.query.join(Access.groups).filter_by(slug=slug)
    models = Model.query.order_by('name').all()
    return render_template("settings/group.html", group=group, title=_(str(group.name) + ' | Olam ERP'), access_rights=access_rights, slug=group.slug, page="group_rights", models=models)


@bp.route("/users", methods=['GET', 'POST'])
def manage_users():
    users = Users.query.join(Partner).all()
    return render_template("settings/users.html", title=_("Users | Olam ERP"), users=users)


@bp.route("/user/<slug>", methods=['GET', 'POST'])
def user(slug):
    user = Users.query.filter_by(slug=slug).first()
    users = Users.query.filter_by(is_archived=False).all()
    for idx, _user in enumerate(users):
        if user.id == _user.id:
            current_index = idx
            prev_index = current_index - 1
            next_index = current_index + 1
    partner = Partner.query.filter_by(id=user.partner_id).first()
    return render_template("settings/user.html", title=_(partner.name + " | Olam ERP"), user=user, partner=partner, users=users, current_index=current_index+1, prev_index=prev_index, next_index=next_index, page="groups")


@bp.route("/edit/user/<slug>", methods=['GET', 'POST'])
def edit_user(slug):
    pass


@bp.route("/new/user", methods=['GET', 'POST'])
def create_user():
    pass
