from app.mixins import BaseModel
from app.extensions import db

class Category(BaseModel):
    __tablename__="categories"

    name = db.Column(db.String(100), unique=True, nullable=False)
    description= db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    products = db.relationship("Product", back_populates="category", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Category, {self.name}>"
