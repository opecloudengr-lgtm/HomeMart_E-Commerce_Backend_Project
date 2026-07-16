from app.mixins import BaseModel
from app.extensions import db

class CartItem(BaseModel):
    __tablename__="cart_items"

    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    cart = db.relationship("Cart", back_populates="cart_items")
    product = db.relationship("Product", back_populates="cart_items")

    def __repr__(self):
        return f"<CartItem Cart: {self.cart_id}, Product: {self.product_id}, Quantity: {self.quantity}>"