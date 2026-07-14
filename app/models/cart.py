from app.mixins import BaseModel
from app.extensions import db

class Cart(BaseModel):
    __tablename__="carts"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="cart")
    cart_items = db.relationship("CartItem", back_populates="cart", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Cart User ID: {self.user_id}>"