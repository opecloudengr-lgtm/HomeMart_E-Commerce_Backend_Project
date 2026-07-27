import uuid
from datetime import datetime, timezone
from app.extensions import db

class PaymentStatus:
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, unique=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    method = db.Column(db.String(30), nullable=False, default="card")
    status = db.Column(db.String(20), nullable=False, default=PaymentStatus.PENDING)
    transaction_ref = db.Column(
        db.String(64), unique=True, nullable=False,
        default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
