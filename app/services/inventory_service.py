from app.extensions import db
from app.models.inventory import Inventory

class InventoryService:
    @staticmethod
    def get_all_inventories():
        return Inventory.query.all()

    @staticmethod
    def get_inventory_by_id(inventory_id):
        return Inventory.query.get(inventory_id)
    
    @staticmethod
    def get_by_product_id(product_id):
        return Inventory.query.filter_by(product_id=product_id).first()
    
    @staticmethod
    def get_low_stock_(threshold=10):
         return Inventory.query.filter_by(Inventory.quantity <= threshold, Inventory.quantity > 0).all()

    @staticmethod
    def get_out_of_stock():
        return Inventory.query.filter_by(Inventory.quantity == 0).all()

    @staticmethod
    def create_inventory(data):
        new_inventory = Inventory(**data)
        db.session.add(new_inventory)
        db.session.commit()
        return new_inventory

    @staticmethod
    def update_inventory(inventory, data):
        for key, value in data.items():
                setattr(inventory, key, value)
        db.session.commit()
        return inventory

    @staticmethod
    def delete_inventory(inventory):
            db.session.delete(inventory)
            db.session.commit()