from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity

from app.models import CartItem, WishlistItem, Order, OrderStatus
from app.schemas import orders_schema
from app.utils.decorators import role_required

customer_bp = Blueprint("customer", __name__, url_prefix="/customer")


@customer_bp.route("/dashboard", methods=["GET"])
@role_required("customer")
def dashboard():
    user_id = get_jwt_identity()

    cart_count = CartItem.query.filter_by(user_id=user_id).count()
    wishlist_count = WishlistItem.query.filter_by(user_id=user_id).count()

    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    total_spent = sum(float(o.total_amount) for o in orders if o.status != OrderStatus.CANCELLED)

    recent_orders = orders[:5]  # only the 5 most recent, for a quick glance

    return jsonify({
        "cart_item_count": cart_count,
        "wishlist_item_count": wishlist_count,
        "total_orders": len(orders),
        "total_spent": total_spent,
        "recent_orders": orders_schema.dump(recent_orders),
    }), 200
