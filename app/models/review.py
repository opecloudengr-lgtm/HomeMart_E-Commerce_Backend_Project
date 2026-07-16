from app.mixins import BaseModel
from app.extensions import db

class Review(BaseModel):
    __tablename__ = "reviews"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    user = db.relationship("User", back_populates="reviews")
    product = db.relationship("Product", back_populates="reviews")
    

    def __repr__(self):
        return f"<Review Product ID: {self.product_id}, Rating: {self.rating}>"