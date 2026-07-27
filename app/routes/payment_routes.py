from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models import Order, OrderStatus, Payment, PaymentStatus
from app.schemas import payment_schema, order_schema
from app.utils.decorators import role_required

payment_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payment_bp.route("/pay/<int:order_id>", methods=["POST"])
@role_required("customer")
def pay_for_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first_or_404()

    if order.status != OrderStatus.PENDING:
        return jsonify({"error": f"This order is already '{order.status}' and cannot be paid again"}), 400

    data = request.get_json() or {}
    method = data.get("method", "card")

    payment = Payment(
        order_id=order.id,
        amount=order.total_amount,
        method=method,
        status=PaymentStatus.SUCCESS,
    )
    db.session.add(payment)

    # Payment succeeded -> move the order forward.
    order.status = OrderStatus.PAID
    db.session.commit()

    return jsonify({
        "message": "Payment successful",
        "payment": payment_schema.dump(payment),
        "order": order_schema.dump(order),
    }), 200


@payment_bp.route("/<int:order_id>", methods=["GET"])
@role_required("customer")
def get_payment(order_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first_or_404()

    if not order.payment:
        return jsonify({"error": "No payment has been made for this order yet"}), 404

    return jsonify(payment_schema.dump(order.payment)), 200
