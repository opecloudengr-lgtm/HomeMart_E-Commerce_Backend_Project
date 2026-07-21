from marshmallow import fields, validate
from app.extensions import ma
from app.models.product import Product

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = False
        include_fk = True

    id = fields.String(dump_only=True)

    name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=255)
    )

    description = fields.String(allow_none=True)

    price = fields.Decimal(
        required=True,
        places=2,
        validate=validate.Range(min=0.01)
    )

    category_id = fields.String(required=True)

    brand_id = fields.String(allow_none=True)

    is_active = fields.Boolean()

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)