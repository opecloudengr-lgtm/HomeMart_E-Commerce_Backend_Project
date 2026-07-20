from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User
from app.constants.roles import Role


def _get_current_user():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    return User.query.get(user_id)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = _get_current_user()
        if not user or user.role not in (Role.ADMIN, Role.SUPER_ADMIN):
            return jsonify({"success": False, "message": "Admin access required."}), 403
        return fn(*args, **kwargs)
    return wrapper


def super_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = _get_current_user()
        if not user or user.role != Role.SUPER_ADMIN:
            return jsonify({"success": False, "message": "Super admin access required."}), 403
        return fn(*args, **kwargs)
    return wrapper


def active_user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = _get_current_user()
        if not user or not user.is_active:
            return jsonify({"success": False, "message": "Account is inactive."}), 403
        return fn(*args, **kwargs)
    return wrapper


def verified_user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = _get_current_user()
        if not user or not user.is_verified:
            return jsonify({"success": False, "message": "Account not verified."}), 403
        return fn(*args, **kwargs)
    return wrapper