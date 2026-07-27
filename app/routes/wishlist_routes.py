from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.extensions import db
from app.models import WishlistItem, Product, CartItem
from app.schemas import wishlist_item_schema, wishlist_items_schema, cart_item_schema
from app.utils.decorators import role_required

wishlist_bp = Blueprint("wishlist", __name__, url_prefix="/wishlist")


@wishlist_bp.route("", methods=["GET"])
@role_required("customer")
def view_wishlist():
    user_id = get_jwt_identity()
    items = WishlistItem.query.filter_by(user_id=user_id).all()
    return jsonify(wishlist_items_schema.dump(items)), 200


@wishlist_bp.route("/add", methods=["POST"])
@role_required("customer")
def add_to_wishlist():
    user_id = get_jwt_identity()
    product_id = (request.get_json() or {}).get("product_id")

    if not product_id:
        return jsonify({"error": "product_id is required"}), 400

    product = Product.query.filter_by(id=product_id, is_active=True).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404

    existing = WishlistItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        return jsonify({"message": "Already in wishlist", "item": wishlist_item_schema.dump(existing)}), 200

    item = WishlistItem(user_id=user_id, product_id=product_id)
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Added to wishlist", "item": wishlist_item_schema.dump(item)}), 201


@wishlist_bp.route("/<int:item_id>", methods=["DELETE"])
@role_required("customer")
def remove_from_wishlist(item_id):
    user_id = get_jwt_identity()
    item = WishlistItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item removed from wishlist"}), 200


@wishlist_bp.route("/<int:item_id>/move-to-cart", methods=["POST"])
@role_required("customer")
def move_to_cart(item_id):
    user_id = get_jwt_identity()
    wishlist_item = WishlistItem.query.filter_by(id=item_id, user_id=user_id).first_or_404()

    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=wishlist_item.product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=user_id, product_id=wishlist_item.product_id, quantity=1)
        db.session.add(cart_item)

    db.session.delete(wishlist_item)
    db.session.commit()

    return jsonify({"message": "Moved to cart", "item": cart_item_schema.dump(cart_item)}), 200
