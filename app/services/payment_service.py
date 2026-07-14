from app.extensions import db
from app.models.payment import Payment

class PaymentService:
    @staticmethod
    def get_all_payment():
        return Payment.query.all()
    
    @staticmethod
    def get_by_payment_id(payment_id):
        return Payment.query.get(payment_id)
    
    @staticmethod
    def get_by_order_id(order_id):
        return Payment.query.filter_by(order_id=order_id).first()
    
    @staticmethod
    def create_payment(data):
        new_payment = Payment(**data)
        db.session.add(new_payment)
        db.session.commit()
        return new_payment
    
    @staticmethod
    def verify_payment(payment, transaction_reference):
        payment.payment_status = 'successful'
        payment.transaction_reference = transaction_reference
        db.session.commit()
        return payment
    
    @staticmethod
    def refund_payment(payment):
        payment.payment_status = 'refunded'
        db.session.commit()
        return payment
    
    @staticmethod
    def delete_payment(payment):
        db.session.delete(payment)
        db.session.commit()