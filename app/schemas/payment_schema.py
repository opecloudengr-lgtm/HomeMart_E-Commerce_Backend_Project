from marshmallow import fields
from app.extensions import ma
from app.models.payment import Payment

class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        load_instance = True
        include_fk =True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    payment_schema = PaymentSchema()
    payments_schema = PaymentSchema(many=True)