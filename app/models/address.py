from app.mixins import BaseModel
from app.extensions import db
from app.models.user import User

class Address(BaseModel):
    __tablename__="addresses"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    user = db.relationship("User", back_populates="addresses")
    orders = db.relationship("Order", back_populates="address", lazy=True)

    def __repr__(self):
        return f"<Address{self.city}, {self.country}>"