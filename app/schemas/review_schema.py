from marshmallow import fields
from app.extensions import ma
from app.models.review import Review

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        load_instance = True
        include_fk =True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    review_schema = ReviewSchema()
    reviews_schema = ReviewSchema(many=True)