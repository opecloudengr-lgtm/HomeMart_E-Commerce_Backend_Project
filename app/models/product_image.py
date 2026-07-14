from app.mixins import BaseModel
from app.extensions import db

class ProductImage(BaseModel):
    __tablename__ = 'product_images'

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    alt_text = db.Column(db.String(255), nullable=True)
    is_primary = db.Column(db.Boolean, default=False, nullable=False)

    product = db.relationship("Product", back_populates="product_images")

    def __repr__(self):
        return f"<ProductImage Product ID {self.product_id}>"
