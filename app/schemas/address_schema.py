from marshmallow import fields
from app.extensions import ma
from app.models.address import Address

class AddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        load_instance = True
        include_fk = True
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)