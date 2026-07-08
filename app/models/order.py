from app.mixins import BaseModel
from app.extensions import db

class Order(BaseModel):
    __tablename__="orders"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)
    order_number = db.Column(db.String(100), unique=True, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Pending")

    def __repr__(self):
        return f"<Order {self.order_number}>"