from marshmallow import fields
from app.extensions import ma
from app.models.wishlist import Wishlist

class WishlistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wishlist
        load_instance = True
        include_fk =True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

wishlist_schema = WishlistSchema()
wishlists_schema = WishlistSchema(many=True)