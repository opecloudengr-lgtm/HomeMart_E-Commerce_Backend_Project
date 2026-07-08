from app.mixins import BaseModel
from app.extensions import db

class Product(BaseModel):
    __tablename__="products"

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=True)
    discount_price = db.Column(db.Numeric(10, 2), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"