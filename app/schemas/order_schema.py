from app.extensions import ma
from app.models import Order, OrderItem, Payment
from app.schemas.product_schema import ProductSchema


class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        load_instance = False
        include_fk = True   # <-- added (order_id is a FK)
        fields = ("id", "order_id", "amount", "method", "status", "transaction_ref", "created_at")

payment_schema = PaymentSchema()

class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem
        load_instance = False
        include_fk = True   # <-- added (product_id is a FK)
        fields = ("id", "product_id", "quantity", "price", "product")

    product = ma.Nested(ProductSchema, only=("id", "name", "image_url"), dump_only=True)


class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = False
        include_fk = True
        fields = (
            "id", "user_id", "total_amount", "status", "shipping_address",
            "created_at", "items", "payment",
        )

    items = ma.Nested(OrderItemSchema, many=True, dump_only=True)
    payment = ma.Nested(PaymentSchema, dump_only=True)


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)