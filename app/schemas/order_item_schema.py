from marshmallow import fields
from app.extensions import ma
from app.models.order_item import OrderItem

class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        load_instance = True
        include_fk =True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

order_item_schema = OrderItemSchema()
order_items_schema = OrderItemSchema(many=True)