# authentication routes
from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from marshmallow import ValidationError
from app.schemas import register_schema, login_schema
from app.schemas import user_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

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