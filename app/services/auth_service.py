from app.extensions import db
from app.models.user import User
from app.utils.security import hash_password, verify_password
from app.utils.token import generate_access_tokens, generate_refresh_tokens

class AuthService:

    @staticmethod
    def register(data):
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return {"success": False, "message": "Email already exists."}, 409

        data.pop("confirm_password")
        data["password_hash"] = hash_password(data.pop("password"))

        user = User(**data)
        db.session.add(user)
        db.session.commit()

        access_token = generate_access_tokens(user.id)
        refresh_token = generate_refresh_tokens(user.id)

        return {"success": True, "message": "Registration successful.", "access_token": access_token, "refresh_token": refresh_token, "user": user}, 201
    
    @staticmethod
    def login(data):
        user = User.query.filter_by(email=data["email"]).first()

        if not user:
            return {"success": False, "message": "Invalid email or password."}, 401
        if not verify_password(data["password"], user.password_hash):
            return {"success": False, "message": "Invalid email or password."}, 401

        access_token = generate_access_tokens(user.id)
        refresh_token = generate_refresh_tokens(user.id)

        return {"success": True, "message": "Login successful.", "access_token": access_token, "refresh_token": refresh_token, "user": user}, 200