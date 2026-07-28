from datetime import datetime, timezone
from app.extensions import db


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    # "jti" = JWT ID, a unique identifier automatically embedded in every
    # token Flask-JWT-Extended issues. This is what we check against.
    jti = db.Column(db.String(36), nullable=False, index=True, unique=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))