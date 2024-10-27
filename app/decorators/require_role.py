from flask import request, jsonify
from functools import wraps

from app.config import USER_ROLES


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = request.headers.get('X-User-Role')
            if user_role not in USER_ROLES:
                return jsonify({'message': 'Unauthorized'}), 401

            if required_role not in USER_ROLES[user_role]:
                return jsonify({'message': 'Forbidden'}), 403
            return f(*args, **kwargs)

        return decorated_function

    return decorator
