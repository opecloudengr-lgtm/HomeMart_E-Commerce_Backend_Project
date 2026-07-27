from datetime import datetime, timezone
from app.extensions import db

class OrderStatus:
    """Possible states an order can move through."""
    PENDING = "pending"          
    PAID = "paid"                
    SHIPPED = "shipped"         
    DELIVERED = "delivered"      
    CANCELLED = "cancelled"      


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    total_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)

    status = db.Column(db.String(20), nullable=False, default=OrderStatus.PENDING)
    shipping_address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    items = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")
    payment = db.relationship("Payment", backref="order", uselist=False, cascade="all, delete-orphan")

class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    product = db.relationship("Product")
