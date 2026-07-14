from app.extensions import db
from app.models.order import Order

class OrderService:
    @staticmethod
    def get_all_orders():
        return Order.query.all()

    @staticmethod
    def get_order_by_id(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def get_order_by_user_id(user_id):
        return Order.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_order(data):
        new_order = Order(**data)
        db.session.add(new_order)
        db.session.commit()
        return new_order

    @staticmethod
    def update_order(order, data):
        for key, value in data.items():
                setattr(order, key, value)
        db.session.commit()
        return order
    
    @staticmethod
    def cancel_order(order):
        order.status = 'cancelled'
        db.session.commit()
        return order

    @staticmethod
    def delete_order(order):
            db.session.delete(order)
            db.session.commit()