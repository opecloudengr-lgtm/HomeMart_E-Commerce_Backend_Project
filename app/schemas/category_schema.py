from marshmallow import fields
from app.extensions import ma
from app.models.category import Category

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    category_schema = CategorySchema()
    categories_schema = CategorySchema(many=True)