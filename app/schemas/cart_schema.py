from marshmallow import fields
from app.extensions import ma
from app.models.cart import Cart
from app.schemas.cart_item_schema import cart_items_schema


class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        load_instance = True

    id = fields.Integer(dump_only=True)

    cart_items = fields.Nested(
        cart_items_schema,
        dump_only=True
    )

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


cart_schema = CartSchema()
carts_schema = CartSchema(many=True)