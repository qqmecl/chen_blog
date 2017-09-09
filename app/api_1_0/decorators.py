from flask import g
from .errors import forbidden
from functools import wraps

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('Insuficient permission.')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
