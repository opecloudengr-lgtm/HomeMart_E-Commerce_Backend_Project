from app.extensions import db
from app.models.cart import Cart

class CartService:
    @staticmethod
    def get_all_Carts():
        return Cart.query.all()

    @staticmethod
    def get_Cart_by_id(cart_id):
        return Cart.query.get(cart_id)

    @staticmethod
    def create_cart(data):
        new_cart = Cart(**data)
        db.session.add(new_cart)
        db.session.commit()
        return new_cart

    @staticmethod
    def update_Cart(cart, data):
        for key, value in data.items():
                setattr(cart, key, value)
        db.session.commit()
        return cart

    @staticmethod
    def delete_Cart(cart):
            db.session.delete(cart)
            db.session.commit()