from marshmallow import fields
from app.extensions import ma
from app.models.wishlist_item import WishlistItem

class WishlistItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WishlistItem
        load_instance = True
        include_fk =True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    wishlist_item_schema = WishlistItemSchema()
    wishlist_items_schema = WishlistItemSchema(many=True)