from marshmallow import fields
from app.extensions import ma
from app.models.cart import Cart

class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        load_instance = True
        include_fk =True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

cart_schema = CartSchema()
carts_schema = CartSchema(many=True)