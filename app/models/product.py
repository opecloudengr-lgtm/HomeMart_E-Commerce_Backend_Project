from app.mixins import BaseModel
from app.extensions import db

class Product(BaseModel):
    __tablename__="products"

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.String, db.ForeignKey("categories.id"), nullable=False)
    brand_id = db.Column(db.String, db.ForeignKey("brands.id"), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    category = db.relationship("Category", back_populates="products")
    brand = db.relationship("Brand", back_populates="products")
    inventory = db.relationship("Inventory", back_populates="product", uselist=False, cascade="all, delete-orphan")
    product_images = db.relationship("ProductImage", back_populates="product", cascade="all, delete-orphan", lazy=True)
    reviews = db.relationship("Review", back_populates="product", cascade="all, delete-orphan", lazy=True)
    cart_items = db.relationship("CartItem", back_populates="product", cascade="all, delete-orphan", lazy=True)
    wishlist_items = db.relationship("WishlistItem", back_populates="product", cascade="all, delete-orphan", lazy=True)
    order_items = db.relationship("OrderItem", back_populates="product", lazy=True)
    discounts = db.relationship(
        "Discount", secondary="product_discounts", back_populates="products", lazy=True
    )

    def __repr__(self):
        return f"<Product {self.id}: {self.name}>"