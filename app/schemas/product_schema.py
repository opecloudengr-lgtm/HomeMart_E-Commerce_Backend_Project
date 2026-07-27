from app.extensions import ma
from app.models import Category, Product

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = False
        fields = ("id", "name", "description")

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

class ProductSchema(ma.SQLAlchemyAutoSchema):
    category = ma.Nested(CategorySchema, only=("id", "name"), dump_only=True)

    class Meta:
        model = Product
        load_instance = False
        include_fk = True
        fields = (
            "id", "name", "description", "price", "stock", "image_url",
            "is_active", "category_id", "category", "created_by",
            "created_at", "updated_at",
        )
        category = ma.Nested(CategorySchema, only=("id", "name"), dump_only=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)