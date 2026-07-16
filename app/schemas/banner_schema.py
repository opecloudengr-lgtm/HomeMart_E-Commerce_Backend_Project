from marshmallow import fields
from app.extensions import ma
from app.models.banner import Banner

class BannerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Banner
        load_instance = True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

banner_schema = BannerSchema()
banners_schema = BannerSchema(many=True)