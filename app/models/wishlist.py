from app.mixins import BaseModel
from app.extensions import db

class Wishlist(BaseModel):
    __tablename__="wishlist"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    user = db.relationship("User", back_populates="wishlist")
    wishlist_items = db.relationship("WishlistItem", back_populates="wishlist", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Wishlist User ID: {self.user_id}>"