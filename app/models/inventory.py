from app.mixins import BaseModel
from app.extensions import db

class Inventory(BaseModel):
    __tablename__="inventories"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False, default=0.0)
    low_stock_threshold = db.Column(db.Integer, nullable=False, default=10)

    def __repr__(self):
        return f"<Inventory Product ID: {self.product_id}, Quantity: {self.quantity}, Price: {self.price}, Low Stock Threshold: {self.low_stock_threshold}>"