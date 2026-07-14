from app.extensions import db
from app.models.order_item import OrderItem

class OrderItemService:
    @staticmethod
    def get_all_order_items():
        return OrderItem.query.all()

    @staticmethod
    def get_order_item_by_id(item_id):
        return OrderItem.query.get(item_id)
    
    @staticmethod
    def get_order_items(order_id):
         return OrderItem.query.filter_by(order_id=order_id).all()

    @staticmethod
    def create_order_item(data):
        new_order_item = OrderItem(**data)
        db.session.add(new_order_item)
        db.session.commit()
        return new_order_item

    @staticmethod
    def update_order_item(order_item, data):
        for key, value in data.items():
                setattr(order_item, key, value)
        db.session.commit()
        return order_item

    @staticmethod
    def delete_order_item(order_item):
            db.session.delete(order_item)
            db.session.commit()