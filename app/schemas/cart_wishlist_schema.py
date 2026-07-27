from app.extensions import ma
from app.models import CartItem, WishlistItem
from app.schemas.product_schema import ProductSchema

class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem
        load_instance = False
        include_fk = True   # <-- added
        fields = ("id", "user_id", "product_id", "quantity", "added_at", "product")

    product = ma.Nested(ProductSchema, dump_only=True)

cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)

class WishlistItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WishlistItem
        load_instance = False
        include_fk = True
        fields = ("id", "user_id", "product_id", "added_at", "product")

    product = ma.Nested(ProductSchema, dump_only=True)

wishlist_item_schema = WishlistItemSchema()
wishlist_items_schema = WishlistItemSchema(many=True)