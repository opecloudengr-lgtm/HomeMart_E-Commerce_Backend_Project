from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models import CartItem, Product
from app.schemas import cart_item_schema, cart_items_schema
from app.utils.decorators import role_required

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


@cart_bp.route("", methods=["GET"])
@role_required("customer")
def view_cart():
    user_id = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=user_id).all()

    # Handy running total so the frontend doesn't have to calculate it.
    total = sum(float(item.product.price) * item.quantity for item in items)

    return jsonify({
        "items": cart_items_schema.dump(items),
        "total": total,
    }), 200


@cart_bp.route("/add", methods=["POST"])
@role_required("customer")
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id or quantity < 1:
        return jsonify({"error": "product_id is required and quantity must be >= 1"}), 400

    product = Product.query.filter_by(id=product_id, is_active=True).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    if not product.is_in_stock(quantity):
        return jsonify({"error": "Not enough stock available"}), 400

    existing = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        existing.quantity += quantity
    else:
        existing = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(existing)

    db.session.commit()
    return jsonify({"message": "Added to cart", "item": cart_item_schema.dump(existing)}), 201

@cart_bp.route("/<int:item_id>", methods=["PATCH"])
@role_required("customer")
def update_cart_item(item_id):
    """Changes the quantity of one item already in the cart."""
    user_id = get_jwt_identity()
    item = CartItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()

    quantity = (request.get_json() or {}).get("quantity")
    if not quantity or quantity < 1:
        return jsonify({"error": "quantity must be >= 1"}), 400
    if not item.product.is_in_stock(quantity):
        return jsonify({"error": "Not enough stock available"}), 400

    item.quantity = quantity
    db.session.commit()
    return jsonify({"message": "Cart updated", "item": cart_item_schema.dump(item)}), 200

@cart_bp.route("/<int:item_id>", methods=["DELETE"])
@role_required("customer")
def remove_from_cart(item_id):
    """Removes a single item from the cart."""
    user_id = get_jwt_identity()
    item = CartItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item removed from cart"}), 200
