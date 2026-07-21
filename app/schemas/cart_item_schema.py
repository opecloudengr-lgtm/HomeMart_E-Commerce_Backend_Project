from marshmallow import fields, validate
from app.extensions import ma
from app.models.cart_item import CartItem


class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem
        load_instance = True

    id = fields.Integer(dump_only=True)

    product_id = fields.Integer(
        required=True
    )

    quantity = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)