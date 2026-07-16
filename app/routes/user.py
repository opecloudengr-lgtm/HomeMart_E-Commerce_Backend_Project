from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas import user_schema
from app.services import UserService

user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/users"
)

@user_bp.get("/profile")
@jwt_required()
def get_profile():

    current_user_id = get_jwt_identity()
    user = UserService.get_user_by_id(current_user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    return jsonify({"success": True, "data": user_schema.dump(user)})