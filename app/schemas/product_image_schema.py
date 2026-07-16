from marshmallow import fields
from app.extensions import ma
from app.models.product_image import ProductImage

class ProductImageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductImage
        load_instance = True
        include_fk =True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

product_image_schema = ProductImageSchema()
product_images_schema = ProductImageSchema(many=True)