from marshmallow import fields
from app.extensions import ma
from app.models.brand import Brand

class BrandSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Brand
        load_instance = True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

brand_schema = BrandSchema()
brands_schema = BrandSchema(many=True)