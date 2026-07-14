from marshmallow import fields
from app.extensions import ma
from app.models.inventory import Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        include_fk =True

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    inventory_schema = InventorySchema()
    inventories_schema = InventorySchema(many=True)