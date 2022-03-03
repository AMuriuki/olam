from app.auth.models.user import Group
from flask_login import current_user
from app import db


def set_default_user_groups(user):
    groups = Group.query.filter_by(permission=1).all()
    for group in groups:
        group.users.append(user)
        db.session.commit()


