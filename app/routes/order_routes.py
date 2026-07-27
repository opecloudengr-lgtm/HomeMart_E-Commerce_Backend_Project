from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models import CartItem, Order, OrderItem, OrderStatus
from app.schemas import order_schema, orders_schema
from app.utils.decorators import role_required

order_bp = Blueprint("orders", __name__, url_prefix="/orders")


@order_bp.route("/checkout", methods=["POST"])
@role_required("customer")
def checkout():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    shipping_address = data.get("shipping_address")

    if not shipping_address:
        return jsonify({"error": "shipping_address is required"}), 400

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"error": "Your cart is empty"}), 400

    for item in cart_items:
        if not item.product.is_in_stock(item.quantity):
            return jsonify({
                "error": f"'{item.product.name}' does not have enough stock "
                         f"(requested {item.quantity}, available {item.product.stock})"
            }), 400

    order = Order(user_id=user_id, shipping_address=shipping_address, status=OrderStatus.PENDING)
    total_amount = 0

    for item in cart_items:
        order_item = OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price,  # snapshot current price
        )
        order.items.append(order_item)
        total_amount += float(item.product.price) * item.quantity

        item.product.stock -= item.quantity

    order.total_amount = total_amount
    db.session.add(order)

    for item in cart_items:
        db.session.delete(item)

    db.session.commit()

    return jsonify({
        "message": "Order placed successfully. Proceed to payment.",
        "order": order_schema.dump(order),
    }), 201


@order_bp.route("", methods=["GET"])
@role_required("customer")
def my_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify(orders_schema.dump(orders)), 200


@order_bp.route("/<int:order_id>", methods=["GET"])
@role_required("customer")
def order_detail(order_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=user_id).first_or_404()
    return jsonify(order_schema.dump(order)), 200
