import random
from datetime import datetime, timedelta, timezone
from app.extensions import db


class OtpPurpose:
    EMAIL_VERIFICATION = "email_verification"
    PASSWORD_RESET = "password_reset"


OTP_EXPIRY_MINUTES = 10


class Otp(db.Model):
    __tablename__ = "otps"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    code = db.Column(db.String(6), nullable=False)
    purpose = db.Column(db.String(30), nullable=False)

    is_used = db.Column(db.Boolean, default=False, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @staticmethod
    def generate_code():
        return f"{random.randint(0, 999999):06d}"

    @classmethod
    def create_for(cls, email, purpose):
        return cls(
            email=email,
            code=cls.generate_code(),
            purpose=purpose,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRY_MINUTES),
        )

    def is_valid(self, code):
        if self.is_used:
            return False
        if self.code != code:
            return False
        
        expires_at = self.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires_at:
            return False
        return True
