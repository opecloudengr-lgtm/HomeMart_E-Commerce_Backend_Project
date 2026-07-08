from app.mixins import BaseModel
from app.extensions import db

class OrderItem(BaseModel):
    __tablename__="order_items"

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<OrderItem Order ID: {self.order_id}, Product ID: {self.product_id}, Quantity: {self.quantity}>"