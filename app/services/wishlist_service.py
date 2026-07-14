from app.extensions import db
from app.models.wishlist import Wishlist

class WishlistService:
    @staticmethod
    def get_all_wishlists():
        return Wishlist.query.all()

    @staticmethod
    def get_wishlist_by_id(wishlist_id):
        return Wishlist.query.get(wishlist_id)
    
    @staticmethod
    def get_wishlist_by_user_id(user_id):
        return Wishlist.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_wishlist(data):
        new_wishlist = Wishlist(**data)
        db.session.add(new_wishlist)
        db.session.commit()
        return new_wishlist

    @staticmethod
    def update_wishlist(wishlist, data):
        for key, value in data.items():
                setattr(wishlist, key, value)
        db.session.commit()
        return wishlist

    @staticmethod
    def delete_wishlist(wishlist):
            db.session.delete(wishlist)
            db.session.commit()