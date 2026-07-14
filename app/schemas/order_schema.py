from marshmallow import fields
from app.extensions import ma
from app.models.order import Order

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
        include_fk =True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    order_schema = OrderSchema()
    orders_schema = OrderSchema(many=True)