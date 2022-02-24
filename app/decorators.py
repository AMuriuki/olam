from functools import wraps
from flask import abort, request
from flask_login import current_user
from app.auth.models.user import Permission
from app import create_app, current_app

app = create_app()


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.has_permission(permission) == False:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def module_access_required(module):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.module_access(module) == False:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def model_access_required(model):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.model_access(model) == False:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def can_create_access_required(model):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.create_access(model) == False:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
