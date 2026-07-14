from app.mixins import BaseModel
from app.extensions import db

class WishlistItem(BaseModel):
    __tablename__="wishlist_items"

    wishlist_id = db.Column(db.Integer, db.ForeignKey("wishlist.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    wishlist = db.relationship("Wishlist", back_populates="wishlist_items")
    product = db.relationship("Product", back_populates="wishlist_items")

    def __repr__(self):
        return f"<WishlistItem Wishlist: {self.wishlist_id}, Product: {self.product_id}>"