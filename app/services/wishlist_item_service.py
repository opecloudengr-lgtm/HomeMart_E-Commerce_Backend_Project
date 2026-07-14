from app.extensions import db
from app.models.wishlist_item import WishlistItem


class WishlistItemService:

    @staticmethod
    def get_all():
        return WishlistItem.query.all()

    @staticmethod
    def get_by_id(item_id):
        return WishlistItem.query.get(item_id)

    @staticmethod
    def get_by_wishlist(wishlist_id):
        return WishlistItem.query.filter_by(
            wishlist_id=wishlist_id
        ).all()

    @staticmethod
    def create(data):
        wishlist_item = WishlistItem(**data)
        db.session.add(wishlist_item)
        db.session.commit()
        return wishlist_item

    @staticmethod
    def delete(wishlist_item):
        db.session.delete(wishlist_item)
        db.session.commit()