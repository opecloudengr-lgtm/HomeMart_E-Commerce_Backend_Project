from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt,
)
from app.extensions import db
from app.models import User, Role, Otp, OtpPurpose, TokenBlocklist
from app.schemas import user_schema
from app.utils.mailer import send_otp_email

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """Public sign-up endpoint. Always creates a CUSTOMER account."""
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists"}), 409

    user = User(name=name, email=email, role=Role.CUSTOMER)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    otp = Otp.create_for(email=user.email, purpose=OtpPurpose.EMAIL_VERIFICATION)
    db.session.add(otp)
    db.session.commit()
    send_otp_email(user.email, otp.code, OtpPurpose.EMAIL_VERIFICATION)

    return jsonify({
        "message": "Registration successful. A verification code has been sent to your email.",
        "user": user_schema.dump(user),
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"error": "This account has been deactivated"}), 403

    extra_claims = {"role": user.role}
    access_token = create_access_token(identity=str(user.id), additional_claims=extra_claims)
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims=extra_claims)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_schema.dump(user),
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    claims = get_jwt()
    new_access_token = create_access_token(
        identity=identity, additional_claims={"role": claims.get("role")}
    )
    return jsonify({"access_token": new_access_token}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user)), 200

@auth_bp.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json() or {}
    email = data.get("email")
    purpose = data.get("purpose")

    if not email or purpose not in (OtpPurpose.EMAIL_VERIFICATION, OtpPurpose.PASSWORD_RESET):
        return jsonify({
            "error": "email is required and purpose must be 'email_verification' or 'password_reset'"
        }), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "If that email is registered, a code has been sent."}), 200

    otp = Otp.create_for(email=email, purpose=purpose)
    db.session.add(otp)
    db.session.commit()
    send_otp_email(email, otp.code, purpose)

    return jsonify({"message": "If that email is registered, a code has been sent."}), 200

@auth_bp.route("/verify-email", methods=["POST"])
def verify_email():
    data = request.get_json() or {}
    email = data.get("email")
    code = data.get("otp")

    if not email or not code:
        return jsonify({"error": "email and otp are required"}), 400

    otp = (
        Otp.query.filter_by(email=email, purpose=OtpPurpose.EMAIL_VERIFICATION, is_used=False)
        .order_by(Otp.created_at.desc())
        .first()
    )

    if not otp or not otp.is_valid(code):
        return jsonify({"error": "Invalid or expired OTP"}), 400

    user = User.query.filter_by(email=email).first_or_404()
    user.is_email_verified = True
    otp.is_used = True
    db.session.commit()

    return jsonify({"message": "Email verified successfully", "user": user_schema.dump(user)}), 200


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json() or {}
    email = data.get("email")
    code = data.get("otp")
    new_password = data.get("new_password")

    if not email or not code or not new_password:
        return jsonify({"error": "email, otp and new_password are required"}), 400

    otp = (
        Otp.query.filter_by(email=email, purpose=OtpPurpose.PASSWORD_RESET, is_used=False)
        .order_by(Otp.created_at.desc())
        .first()
    )

    if not otp or not otp.is_valid(code):
        return jsonify({"error": "Invalid or expired OTP"}), 400

    user = User.query.filter_by(email=email).first_or_404()
    user.set_password(new_password)
    otp.is_used = True
    db.session.commit()

    return jsonify({"message": "Password reset successfully. You can now log in with your new password."}), 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route("/logout-refresh", methods=["POST"])
@jwt_required(refresh=True)
def logout_refresh():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return jsonify({"message": "Refresh token revoked successfully"}), 200
