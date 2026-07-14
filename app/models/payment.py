from app.mixins import BaseModel
from app.extensions import db

class Payment(BaseModel):
    __tablename__="payments"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default="Pending")
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)

    order = db.relationship("Order", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.transaction_id}>"