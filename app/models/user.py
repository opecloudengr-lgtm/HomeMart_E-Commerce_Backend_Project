from werkzeug.security import generate_password_hash, check_password_hash
from app.mixins import BaseModel
from app.extensions import db

class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="customer")
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    addresses = db.relationship("Address", back_populates="user", cascade="all, delete-orphan", lazy=True)
    cart = db.relationship("Cart", back_populates="user", uselist=False, cascade="all, delete-orphan")
    wishlist = db.relationship("Wishlist", back_populates="user", uselist=False, cascade="all, delete-orphan")
    orders = db.relationship("Order", back_populates="user", cascade="all, delete-orphan", lazy=True)
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan", lazy=True) 

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f"<User{self.email}>"