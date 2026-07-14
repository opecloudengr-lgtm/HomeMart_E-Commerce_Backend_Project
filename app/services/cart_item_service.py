from app.extensions import db
from app.models import cart_item
from app.models.cart_item import CartItem

class CartItemService:
    @staticmethod
    def get_all_CartItemes():
        return CartItem.query.all()

    @staticmethod
    def get_cart_item_by_id(item_id):
        return CartItem.query.get(item_id)

    @staticmethod
    def create_cart_item(data):
        new_cart_item = CartItem(**data)
        db.session.add(new_cart_item)
        db.session.commit()
        return new_cart_item

    @staticmethod
    def update_cart_item(cart_item, data):
        for key, value in data.items():
                setattr(cart_item, key, value)
        db.session.commit()
        return cart_item

    @staticmethod
    def delete_cart_item(cart_item):
            db.session.delete(cart_item)
            db.session.commit()