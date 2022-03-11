from functools import wraps
from flask import abort
from flask_login import current_user, logout_user


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


def can_write_access_required(model):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.write_access(model) == False:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def active_user_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_archived == True:
            logout_user()
            abort(403)
        return func(*args, **kwargs)
    return decorated_function
