# authentication routes
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from marshmallow import ValidationError
from app.schemas import register_schema, login_schema
from app.schemas import user_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import change_password_schema
from app.schemas import forgot_password_schema
from app.schemas import reset_password_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/register")
def register():
    try:
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"success": False, "error": err.messages}), 400
    
    response, status = AuthService.register(data)
    if response["success"]:
        response["user"] = user_schema.dump(response["user"])
    return jsonify(response), status

@auth_bp.post("/login")
def login():
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"success": False, "error": err.messages}), 400
    
    response, status = AuthService.login(data)
    if response["success"]:
        response["user"]=user_schema.dump(response["user"])
    return jsonify(response), status

@auth_bp.post("/refresh-token")
@jwt_required(refresh=True)
def refresh_token():
    current_user_id = get_jwt_identity()
    response, status = AuthService.refresh_token(current_user_id)
    return jsonify(response), status

@auth_bp.post("/logout")
@jwt_required()
def logout():
    response, status = AuthService.logout()
    return jsonify(response), status

@auth_bp.put("/change-password")
@jwt_required()
def change_password():

    try:
        data = change_password_schema.load(request.get_json())

    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    user_id = get_jwt_identity()

    response, status = AuthService.change_password(user_id, data)
    return jsonify(response), status

@auth_bp.post("/forgot-password")
def forgot_password():

    try:
        data = forgot_password_schema.load(request.get_json())

    except ValidationError as err:
        return jsonify({"success": False, "errors": err.messages}), 400

    response, status = AuthService.forgot_password(data)

    return jsonify(response), status

@auth_bp.post("/reset-password")
def reset_password():

    try:
        data = reset_password_schema.load(
            request.get_json()
        )

    except ValidationError as err:
        return jsonify(
            {
                "success": False,
                "errors": err.messages
            }
        ), 400

    response, status = AuthService.reset_password(data)

    return jsonify(response), status

@auth_bp.get("/verify-email")
def verify_email():

    token = request.args.get("token")

    if not token:
        return jsonify(
            {
                "success": False,
                "message": "Verification token is required."
            }
        ), 400

    response, status = AuthService.verify_email(token)

    return jsonify(response), status