from crypt import methods
import uuid
import requests
from flask.json import jsonify
from itsdangerous import json
from sqlalchemy import log
from app import db, api_base
from app.auth.email import send_invite_email
from app.decorators import can_create_access_required, can_write_access_required, module_access_required, model_access_required, permission_required
from app.helper_functions import set_default_user_groups
from app.main.models.module import Model
from app.main.models.partner import Partner
from app.settings import bp
from flask_login import login_required, current_user
from flask import current_app, render_template, redirect, url_for, request, session, flash
from app.settings.forms import InviteForm, NewGroup, NewUserForm
from flask_babel import _, lazy_gettext as _l
from app.auth.models.user import USERTYPES, Access, Permission, UserType, Users, Group, FILTERS

selected_groups = {}


@bp.route("/get_models", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def get_models():
    if request.method == "POST":
        models = Model.to_collection_dict(Model.query.order_by('name'))
        return jsonify(models)


@bp.route('/', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def settings():
    form = InviteForm()
    pending_invitations = Users.query.filter_by(is_active=False).all()
    return render_template('settings/settings.html', title=_('General Settings | Olam ERP'), form=form, pending_invitations=pending_invitations)


@bp.route('/invite', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
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
@module_access_required(1)
def manage_groups():
    groups = Group.query.filter_by(
        is_active=True).order_by(Group.module_id).all()
    return render_template("settings/groups.html", title=_('Groups | Olam ERP'), groups=groups)


@bp.route('/new_group', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def new_group():
    form = NewGroup()
    group = None
    models = Model.query.order_by('name').all()
    permissions = Permission

    if form.validate_on_submit():
        exists = Group.query.filter_by(
            name=request.form['group_name']).filter_by(module_id=request.form['select_app']).filter_by(is_active=True).first()
        if exists:
            flash(
                _('A group with this details exists.'))
            return jsonify({"response": "group name exists!"})
        else:
            group = Group(id=uuid.uuid4(
            ), name=request.form['group_name'], module_id=request.form['select_app'], permisssion=request.form['select_permission'])
            group.generate_slug()
            db.session.add(group)
            db.session.commit()
            flash(
                _('Your group has been created successfully.'))
            return jsonify({"response": "success", "slug": group.slug})
    return render_template("settings/new_group.html", title=_('New Group | Olam ERP'), group=group, form=form, models=models, permissions=permissions)


@bp.route('/new_group/<slug>', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def newgroup(slug):
    form = NewGroup()
    group = Group.query.filter_by(slug=slug).first()
    group_members = Users.query.join(Users.groups).filter_by(slug=slug)
    access_rights = Access.query.join(Access.groups).filter_by(slug=slug)
    models = Model.query.order_by('name').all()
    if form.validate_on_submit():
        exists = Group.query.filter_by(
            name=request.form['group_name']).filter_by(is_active=True).filter_by(module_id=request.form['select_app']).filter(Group.id != group.id).first()
        if exists:
            flash(
                _('A group with this details exists.'))
            return jsonify({"response": "group name exists!"})
        else:
            group.name = request.form['group_name']
            group.module_id = request.form['select_app']
            group.permission = request.form['select_permission']
            db.session.commit()
            flash(
                _('This group has been saved successfully.'))
            return jsonify({"response": "success", "slug": group.slug})
    return render_template("settings/new_group.html", group=group, title=_('New Group | Olam ERP'), group_members=group_members, slug=slug, form=form, models=models, access_rights=access_rights)


@bp.route("/settings/update/<slug>", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def update_group(slug):
    form = NewGroup()
    group = Group.query.filter_by(slug=slug).first()
    if form.validate_on_submit():
        exists = Group.query.filter_by(
            name=request.form['group_name']).filter_by(module_id=request.form['select_app']).filter_by(is_active=True).filter(Group.id != group.id).first()
        if exists:
            flash(
                _('A group with this details exists.'))
            return jsonify({"response": "group name exists!", "slug": slug})
        else:
            group.name = request.form['group_name']
            group.module_id = request.form['select_app']
            db.session.commit()
            return jsonify({"response": "success"})
    return redirect(url_for('settings.group', slug=slug))


@bp.route('/group/<slug>', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def group(slug):
    group = Group.query.filter_by(slug=slug).first()
    group_members = Users.query.join(Users.groups).filter_by(slug=slug)
    access_rights = Access.query.join(Access.groups).filter_by(slug=slug)
    models = Model.query.order_by('name').all()
    if not group:
        return redirect(url_for('settings.new_group'))
    return render_template("settings/group.html", group=group, title=_(str(group.name) + ' | Olam ERP'), group_members=group_members, slug=group.slug, access_rights=access_rights, models=models, page="group_members")


@bp.route('/select_users', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def select_users():
    if request.method == "POST":
        if "slug" in request.form:
            group = Group.query.filter_by(slug=request.form['slug']).first()
        else:
            group = Group(id=uuid.uuid4())
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
@module_access_required(1)
def discard_group(slug):
    group = Group.query.filter_by(slug=slug).first()
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('settings.manage_groups'))


@bp.route('/delete-group', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def delete_group():
    if request.method == "POST":
        selected = request.form.getlist(
            'selected_groups[]')
        for group in selected:
            group = Group.query.filter_by(id=group).first()
            group.is_active = False
            db.session.commit()
        return jsonify({"response": "success"})


@bp.route('/remove_user', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def remove_user():
    if request.method == "POST":
        group = Group.query.filter_by(slug=request.form['slug']).first()
        user = Users.query.filter_by(id=request.form['user_id']).first()
        group.users.remove(user)
        db.session.commit()
        return jsonify({'response': 'success'})


@bp.route('/edit_group/<slug>', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def edit_group(slug):
    edit = True
    form = NewGroup()
    group = Group.query.filter_by(slug=slug).first()
    group_members = Users.query.join(Users.groups).filter_by(slug=slug)
    access_rights = Access.query.join(Access.groups).filter_by(slug=slug)
    models = Model.query.order_by('name').all()
    permissions = Permission
    return render_template("settings/edit_group.html", group=group, title=_("Edit " + str(group.name) + " | Olam ERP"), form=form, group_members=group_members, slug=group.slug, edit=edit, access_rights=access_rights, models=models, permissions=permissions)


@bp.route('/access-right', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def new_access_right():
    if request.method == "POST":
        if "access" in request.form:
            model_name = None
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

            return jsonify({"response": "success", "model_name": model_name, "access": access.id})
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
                access = Access(id=uuid.uuid4(
                ), name=request.form['access_name'], model_id=request.form['model'], read=read, write=write, create=create, delete=delete)
                access.generate_slug()
                db.session.add(access)
                group.rights.append(access)
                db.session.commit()
                return jsonify({"response": "success", "access": access.id})


@bp.route('/remove_access_right', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def remove_access_right():
    if request.method == "POST":
        group = Group.query.filter_by(slug=request.form['group']).first()
        access_right = Access.query.filter_by(
            id=request.form['access']).first()
        group.rights.remove(access_right)
        Access.query.filter_by(id=request.form['access']).delete()
        db.session.commit()
        return jsonify({'response': 'success'})


@bp.route('/group/members/<slug>', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def group_members(slug):
    group = Group.query.filter_by(slug=slug).first()
    group_members = Users.query.join(Users.groups).filter_by(slug=slug)
    return render_template("settings/group.html", group=group, title=_(str(group.name) + ' | Olam ERP'), group_members=group_members, slug=group.slug, page="group_members")


@bp.route('/group/rights/<slug>', methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def group_rights(slug):
    group = Group.query.filter_by(slug=slug).first()
    access_rights = Access.query.join(Access.groups).filter_by(slug=slug)
    models = Model.query.order_by('name').all()
    return render_template("settings/group.html", group=group, title=_(str(group.name) + ' | Olam ERP'), access_rights=access_rights, slug=group.slug, page="group_rights", models=models)


@bp.route("/users", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
@model_access_required(1)
def manage_users():
    filters = FILTERS
    filter_id = request.args.get('filter')
    if filter_id:
        if filter_id == "0":
            users = Users.query.filter_by(is_active=True).filter_by(
                is_archived=True).join(Partner).all()
        elif filter_id == "1":
            users = Users.query.filter_by(is_active=True).filter_by(
                user_type="Internal User").join(Partner).all()
    else:
        users = Users.query.filter_by(is_active=True).join(Partner).all()
    return render_template("settings/users.html", title=_("Users | Olam ERP"), users=users, filters=filters, filter_id=filter_id)


@bp.route("/delete_users", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
@model_access_required(1)
@can_write_access_required(1)
def delete_users():
    if request.method == "POST":
        selected_users = request.form.getlist('selected_users[]')
        for selected_user in selected_users:
            user = Users.query.filter_by(id=int(selected_user)).first()
            if user == current_user:
                return jsonify({"response": "current user"})
            else:
                db.session.delete(user)
                Partner.query.filter_by(id=user.partner_id).delete()
                db.session.commit()
                return jsonify({"response": "success"})


@bp.route("/delete_user", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
@model_access_required(1)
@can_write_access_required(1)
def delete_user():
    if request.method == "POST":
        selected_user = request.form['selected_user']
        user = Users.query.filter_by(slug=selected_user).first()
        if user == current_user:
            return jsonify({"response": "current user"})
        else:
            db.session.delete(user)
            Partner.query.filter_by(id=user.partner_id).delete()
            db.session.commit()
            return jsonify({"response": "success"})


@bp.route("/archive-users", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
@model_access_required(1)
@can_write_access_required(1)
def archive_users():
    if request.method == "POST":
        selected_users = request.form.getlist('selected_users[]')
        for selected_user in selected_users:
            user = Users.query.filter_by(id=int(selected_user)).first()
            if user == current_user:
                return jsonify({"response": "current user"})
            else:
                user.is_active = False
                partner = Partner.query.filter_by(id=user.partner_id).first()
                partner.is_active = False
                db.session.commit()
                return jsonify({"response": "success"})


@bp.route("/archive_user", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
@model_access_required(1)
@can_write_access_required(1)
def archive_user():
    if request.method == "POST":
        selected_user = request.form['selected_user']
        user = Users.query.filter_by(slug=selected_user).first()
        if user == current_user:
            return jsonify({"response": "current user"})
        else:
            user.is_active = False
            partner = Partner.query.filter_by(id=user.partner_id).first()
            partner.is_active = False
            db.session.commit()
            return jsonify({"response": "success"})


@bp.route("/user/<slug>", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def user(slug):
    user = Users.query.filter_by(slug=slug).first()
    user_groups = user.groups
    users = Users.query.filter_by(is_archived=False).all()
    user_types = UserType

    for idx, _user in enumerate(users):
        if user.id == _user.id:
            current_index = idx
            prev_index = current_index - 1
            next_index = current_index + 1
    partner = Partner.query.filter_by(id=user.partner_id).first()
    return render_template("settings/user.html", title=_(partner.name + " | Olam ERP"), user=user, partner=partner, users=users, current_index=current_index+1, prev_index=prev_index, next_index=next_index, page="groups", user_types=user_types, user_groups=user_groups, slug=slug)


@bp.route("/edit/user/<slug>", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def edit_user(slug):
    edit = True
    user = Users.query.filter_by(slug=slug).first()
    partner = Partner.query.filter_by(id=user.partner_id).first()
    users = Users.query.filter_by(is_archived=False).all()
    user_types = UserType
    groups = Group.query.filter_by(is_active=True).all()
    form = NewUserForm()
    for idx, _user in enumerate(users):
        if user.id == _user.id:
            current_index = idx
            prev_index = current_index - 1
            next_index = current_index + 1

    if form.validate_on_submit():
        exists = Partner.query.filter(Partner.id != partner.id).filter_by(
            email=request.form['email']).first()
        if exists:
            return jsonify({"response": "there is a user with this email address!"})
        else:
            partner.name = request.form['name']
            partner.email = request.form['email']
            partner.company_id = current_user.company_id
            partner.is_tenant = True
            db.session.commit()
            group_ids = list(selected_groups.values())
            for group_id in group_ids:
                group = Group.query.filter_by(id=group_id).first()
                group.users.append(user)
                db.session.commit()
            return jsonify({"response": "success", "slug": slug})

    return render_template("settings/edit_user.html", title=_("Edit " + partner.name + " | Olam ERP"), user=user, partner=partner, users=users, current_index=current_index+1, prev_index=prev_index, next_index=next_index, page="groups", user_types=user_types, form=form, edit=edit, groups=groups, slug=slug)


@bp.route("/set-access", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def set_acess():
    if request.method == "POST":
        module_id = request.form['module']
        group_id = request.form['group']
        if group_id != '#':
            selected_groups[module_id] = group_id
        return jsonify({"response": "success"})


@bp.route("/new/user", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
@can_create_access_required(1)
def create_user():
    new_user = True
    user_types = UserType
    form = NewUserForm()
    user = Users.query.filter_by(id=current_user.get_id()).first()
    groups = Group.query.filter_by(is_active=True).all()
    invited_by = Partner.query.filter_by(id=user.partner_id).first()

    if form.validate_on_submit():
        exists = Partner.query.filter_by(email=request.form['email']).first()
        if exists:
            return jsonify({"response": "user email exists!"})
        else:
            partner = Partner(name=request.form['name'], email=request.form['email'],
                              company_id=current_user.company_id, is_tenant=True)
            partner.generate_slug()
            db.session.add(partner)
            db.session.commit()
            user = Users(partner_id=partner.id,
                         company_id=current_user.company_id, user_type=request.form['user-type'])
            user.set_token(partner.id)
            user.generate_slug()
            db.session.add(user)
            db.session.commit()
            send_invite_email(partner.id, invited_by.id)
            group_ids = list(selected_groups.values())
            for group_id in group_ids:
                group = Group.query.filter_by(id=group_id).first()
                group.users.append(user)
                db.session.commit()
            return jsonify({"response": "success"})
    return render_template("settings/new_user.html", title=_("New | Olam ERP"), new_user=new_user, form=form, user_types=user_types, groups=groups)


@bp.route("/apps", methods=['GET', 'POST'])
@login_required
def get_apps():
    response = requests.get(
        api_base + '/api/module_categories')
    response_dict = json.loads(response.content)
    _response = requests.get(
        api_base + '/api/apps')
    _response_dict = json.loads(_response.content)
    return render_template("settings/apps.html", title=_("Apps | Olam ERP"), categories=response_dict['items'], apps=_response_dict['items'])


@bp.route("/re-send-invitation/<slug>", methods=['GET', 'POST'])
@login_required
@module_access_required(1)
def resend_invitation(slug):
    invited_by = Partner.query.filter_by(id=current_user.partner_id).first()
    user = Users.query.filter_by(slug=slug).first()
    partner = Partner.query.filter_by(id=user.partner_id).first()
    send_invite_email(partner.id, invited_by.id)
    flash(_("Invitation email sent"))
    return redirect(url_for("settings.user", slug=slug))
