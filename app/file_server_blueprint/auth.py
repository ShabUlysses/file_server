from functools import wraps

from flask import request, current_app


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == current_app.config['USER_LOGIN'] and auth.password == current_app.config['USER_PASSWORD']:
            return f(*args, **kwargs)
        return "Access denied", 401
    return decorated
