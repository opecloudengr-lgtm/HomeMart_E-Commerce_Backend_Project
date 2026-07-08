from app.mixins import BaseModel
from app.extensions import db

class Cart(BaseModel):
    __tablename__="carts"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Cart User ID: {self.user_id}>"