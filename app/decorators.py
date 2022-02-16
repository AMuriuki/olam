from functools import wraps
from flask import abort
from flask_login import current_user
from app.auth.models.user import Permission
from app.main.models.module import Module


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    # check if user's group any access right to settings module 
    return permission_required(Permission.ADMIN)(f)
