from app.mixins import BaseModel
from app.extensions import db

class Discount(BaseModel):
    __tablename__="discounts"

    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    percentage = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    products = db.relationship(
        "Product", secondary="product_discounts", back_populates="discounts", lazy=True
    )

    def __repr__(self):
        return f"<Discount {self.name}>"