from marshmallow import fields
from app.extensions import ma
from app.models.discount import Discount

class DiscountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Discount
        load_instance = True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

discount_schema = DiscountSchema()
discounts_schema = DiscountSchema(many=True)