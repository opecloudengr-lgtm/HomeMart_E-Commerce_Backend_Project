from app.extensions import db
from app.models.discount import Discount

class DiscountService:
    @staticmethod
    def get_all_discounts():
        return Discount.query.all()

    @staticmethod
    def get_discount_by_id(discount_id):
        return Discount.query.get(discount_id)

    @staticmethod
    def create_discount(data):
        new_discount = Discount(**data)
        db.session.add(new_discount)
        db.session.commit()
        return new_discount

    @staticmethod
    def update_discount(discount, data):
        for key, value in data.items():
                setattr(discount, key, value)
        db.session.commit()
        return discount

    @staticmethod
    def delete_discount(discount):
            db.session.delete(discount)
            db.session.commit()