from datetime import datetime, timedelta
from app.extensions import db
from app.models.user import User
from app.constants.roles import Role
from app.utils.security import generate_reset_token


class UserService:

    @staticmethod
    def get_all():
        users = User.query.order_by(User.created_at.desc()).all()
        return {
            "success": True,
            "count": len(users),
            "users": users
        }, 200

    @staticmethod
    def get_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"success": False, "message": "User not found."}, 404
        return {"success": True, "user": user}, 200

    @staticmethod
    def update_role(user_id, role):
        user = User.query.get(user_id)
        if not user:
            return {"success": False, "message": "User not found."}, 404

        if role not in (Role.CUSTOMER, Role.ADMIN, Role.SUPER_ADMIN):
            return {"success": False, "message": "Invalid role."}, 400

        user.role = role
        db.session.commit()
        return {"success": True, "message": "Role updated successfully.", "user": user}, 200

    @staticmethod
    def deactivate(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"success": False, "message": "User not found."}, 404

        user.is_active = False
        db.session.commit()
        return {"success": True, "message": "User deactivated successfully."}, 200

    @staticmethod
    def activate(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"success": False, "message": "User not found."}, 404

        user.is_active = True
        db.session.commit()
        return {"success": True, "message": "User activated successfully."}, 200

    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"success": False, "message": "User not found."}, 404

        db.session.delete(user)
        db.session.commit()
        return {"success": True, "message": "User deleted successfully."}, 200
    
    @staticmethod
    def update_profile(user_id, data):
        user = db.session.get(User, user_id)

        if not user:
            return {"success": False, "message": "User not found."}, 404

        for key, value in data.items():
            setattr(user, key, value)

        db.session.commit()

        return {"success": True, "message": "Profile updated successfully.", "user": user}, 200

    @staticmethod
    def change_email(user_id, data):
        user = db.session.get(User, user_id)

        if not user:
            return {"success": False, "message": "User not found."}, 404

        existing_user = User.query.filter_by(email=data["email"]).first()

        if existing_user and existing_user.id != user.id:
            return {"success": False, "message": "Email already exists."}, 409

        user.email = data["email"]
        user.is_verified = False
        user.verification_token = generate_reset_token()
        user.verification_token_expires_at = datetime.utcnow() + timedelta(days=1)

        db.session.commit()

        return {
        "success": True,
        "message": "Email updated successfully. Please verify your new email address.",
        "user": user
    }, 200