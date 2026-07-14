from marshmallow import fields
from app.extensions import ma
from app.models.cart_item import CartItem

class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem
        load_instance = True
        include_fk =True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    cart_item_schema = CartItemSchema()
    cart_items_schema = CartItemSchema(many=True)