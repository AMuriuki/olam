import imp
from app import api_base, db
import requests
import json
from app.auth.models.user import Access, Group, Users
from flask_login import current_user
from app.main.models.module import Model, Module


def get_access_groups():
    modules = Module.query.all()
    for module in modules:
        response = requests.get(api_base+module.user_groups_api)
        response_dict = json.loads(response.content)
        for i in range(len(response_dict['items'])):
            exists = Group.query.filter_by(
                id=response_dict['items'][i]['id']).first()
            if not exists:
                group = Group(id=response_dict['items'][i]['id'], name=response_dict['items'][i]['name'],
                              module_id=response_dict['items'][i]['module_id'], permission=response_dict['items'][i]['permission'], access_rights_url=response_dict['items'][i]['links']['access_rights'])
                group.generate_slug()
                db.session.add(group)
                db.session.commit()
                print("Group: "+group.name+" added")


def get_access_rights():
    groups = Group.query.all()
    for group in groups:
        response = requests.get(api_base + group.access_rights_url)
        response_dict = json.loads(response.content)
        for i in range(len(response_dict['items'])):
            exists = Access.query.filter_by(
                id=response_dict['items'][i]['id']).first()
            if not exists:
                access = Access(id=response_dict['items'][i]['id'], name=response_dict['items'][i]['name'], model_id=response_dict['items'][i]['model_id'], read=response_dict['items']
                                [i]['read'], write=response_dict['items'][i]['write'], create=response_dict['items'][i]['create'], delete=response_dict['items'][i]['delete'])
                access.generate_slug()
                db.session.add(access)
                db.session.commit()
                group.rights.append(access)
                db.session.commit()
                print("Access: "+access.name+" added")


def get_models():
    modules = Module.query.all()
    for module in modules:
        response = requests.get(api_base+module.models_api)
        response_dict = json.loads(response.content)
        for i in range(len(response_dict['items'])):
            exists = Model.query.filter_by(id=response_dict['items'][i]['id']).first()
            if not exists:
                model = Model(id=response_dict['items'][i]['id'], name=response_dict['items'][i]['name'],
                            description=response_dict['items'][i]['description'], module_id=response_dict['items'][i]['module_id'])
                model.generate_slug()
                db.session.add(model)
                db.session.commit()
                print("Model: "+model.name+" added")


def set_admin_groups():
    groups = Group.query.filter_by(permission=3).all()
    user = Users.query.filter_by(id=1).first()
    for group in groups:
        group.users.append(user)
        db.session.commit()
