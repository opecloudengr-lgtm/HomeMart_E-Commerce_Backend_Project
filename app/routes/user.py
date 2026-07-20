from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from app.schemas import (
    user_schema,
    users_schema,
    update_profile_schema,
    change_email_schema,
)

from app.services.user_service import UserService

from app.utils.token import get_current_user_id

from app.utils.decorators import (
    admin_required,
    super_admin_required,
)

user_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users"
)

@user_bp.get("/profile")
@jwt_required()
def profile():

    user_id = get_current_user_id()

    response, status = UserService.get_by_id(user_id)

    if response["success"]:
        response["user"] = user_schema.dump(
            response["user"]
        )

    return jsonify(response), status

@user_bp.put("/profile")
@jwt_required()
def update_profile():

    try:
        data = update_profile_schema.load(
            request.get_json()
        )

    except ValidationError as err:
        return jsonify({
            "success": False,
            "errors": err.messages
        }), 400

    user_id = get_current_user_id()

    response, status = UserService.update_profile(
        user_id,
        data
    )

    if response["success"]:
        response["user"] = user_schema.dump(
            response["user"]
        )

    return jsonify(response), status

@user_bp.put("/change-email")
@jwt_required()
def change_email():

    try:
        data = change_email_schema.load(
            request.get_json()
        )

    except ValidationError as err:
        return jsonify({
            "success": False,
            "errors": err.messages
        }), 400

    user_id = get_current_user_id()

    response, status = UserService.change_email(
        user_id,
        data
    )

    if response["success"]:
        response["user"] = user_schema.dump(
            response["user"]
        )

    return jsonify(response), status

@user_bp.get("/")
@admin_required
def get_users():

    response, status = UserService.get_all()

    response["users"] = users_schema.dump(
        response["users"]
    )

    return jsonify(response), status

@user_bp.get("/<string:user_id>")
@admin_required
def get_user(user_id):

    response, status = UserService.get_by_id(
        user_id
    )

    if response["success"]:
        response["user"] = user_schema.dump(
            response["user"]
        )

    return jsonify(response), status

@user_bp.patch("/<string:user_id>/role")
@super_admin_required
def update_role(user_id):

    role = request.get_json().get("role")

    response, status = UserService.update_role(
        user_id,
        role
    )

    if response["success"]:
        response["user"] = user_schema.dump(
            response["user"]
        )

    return jsonify(response), status

@user_bp.patch("/<string:user_id>/activate")
@super_admin_required
def activate_user(user_id):

    response, status = UserService.activate(
        user_id
    )

    return jsonify(response), status

@user_bp.patch("/<string:user_id>/deactivate")
@super_admin_required
def deactivate_user(user_id):

    response, status = UserService.deactivate(
        user_id
    )

    return jsonify(response), status

@user_bp.delete("/<string:user_id>")
@super_admin_required
def delete_user(user_id):

    response, status = UserService.delete(
        user_id
    )

    return jsonify(response), status