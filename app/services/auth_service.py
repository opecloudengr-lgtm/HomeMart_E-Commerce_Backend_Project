from app.extensions import db
from app.models.user import User
from app.utils.security import hash_password, verify_password
from app.utils.token import generate_access_tokens, generate_refresh_tokens
from app.utils.security import (hash_password, verify_password)
from datetime import datetime, timedelta
from app.utils.security import (generate_reset_token)
from app.constants.roles import Role

class AuthService:

    @staticmethod
    def register(data):
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return {"success": False, "message": "Email already exists."}, 409

        data.pop("confirm_password")
        data["password_hash"] = hash_password(data.pop("password"))
        data["role"] = Role.CUSTOMER

        user = User(**data)
        from datetime import datetime, timedelta
        from app.utils.security import generate_reset_token

        user.verification_token = generate_reset_token()

        user.verification_token_expires_at = (datetime.utcnow() + timedelta(days=1))
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
        if not verify_password(user.password_hash, data["current_password"]):
            return {"success": False, "message": "Current password is incorrect."}, 400

        access_token = generate_access_tokens(user.id)
        refresh_token = generate_refresh_tokens(user.id)

        return {"success": True, "message": "Login successful.", "access_token": access_token, "refresh_token": refresh_token, "user": user}, 200
    
    @staticmethod
    def refresh_token(user_id):
        access_token = generate_access_tokens(user_id)
        return{"success": True, "message": "Token refreshed successfully", "access_token": access_token}, 200
    
    @staticmethod
    def logout():
        return{"success": True, "message": "Logout successful."}, 200
    
    @staticmethod
    def change_password(user_id, data):

        user = User.query.get(user_id)

        if not user:
            return {"success": False, "message": "User not found."}, 404

        if not verify_password(user.password_hash, data["current_password"]):
            return {"success": False, "message": "Current password is incorrect."}, 400

        user.password_hash = hash_password(data["new_password"])

        db.session.commit()

        return {"success": True, "message": "Password changed successfully."}, 200
    
    @staticmethod
    def forgot_password(data):

        user = User.query.filter_by(email=data["email"]).first()

        if not user:
            return {"success": False, "message": "User not found."}, 404

        token = generate_reset_token()
        user.reset_token = token
        user.reset_token_expires_at = datetime.utcnow() + timedelta(hours=1)

        db.session.commit()
        return {"success": True, "message": "Password reset instructions have been sent.", "reset_token": token}, 200
    
    @staticmethod
    def reset_password(data):

        user = User.query.filter_by(
        reset_token=data["token"]
        ).first()

        if not user:
            return {
            "success": False,
            "message": "Invalid reset   token."
        }, 400

        if (
        user.reset_token_expires_at is None or
        user.reset_token_expires_at < datetime.utcnow()
    ):
            return {
            "success": False,
            "message": "Reset token has expired."
        }, 400

        user.password = hash_password(
        data["password"]
    )

    # Invalidate the token
        user.reset_token = None
        user.reset_token_expires_at = None

        db.session.commit()
        return {
        "success": True,
        "message": "Password reset successfully."
    }, 200

    @staticmethod
    def verify_email(token):

        user = User.query.filter_by(
        verification_token=token
    ).first()

        if not user:
            return {
            "success": False,
            "message": "Invalid verification token."
        }, 400

        if (
        user.verification_token_expires_at is None or
        user.verification_token_expires_at < datetime.utcnow()
    ):
            return {
            "success": False,
            "message": "Verification token has expired."
        }, 400

        user.is_verified = True

        user.verification_token = None
        user.verification_token_expires_at = None

        db.session.commit()

        return {
        "success": True,
        "message": "Email verified successfully."
    }, 200