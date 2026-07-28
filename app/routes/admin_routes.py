from flask import Blueprint, request, jsonify
from sqlalchemy import func

from app.extensions import db
from app.models import Product, Category, Order, OrderItem, OrderStatus
from app.schemas import product_schema, products_schema, order_schema, orders_schema
from app.utils.decorators import role_required
from flask_jwt_extended import get_jwt_identity

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# PRODUCT MANAGEMENT

@admin_bp.route("/products", methods=["POST"])
@role_required("admin")
def create_product():
    """Admin adds a new product to the store."""
    data = request.get_json() or {}
    name = data.get("name")
    price = data.get("price")

    if not name or price is None:
        return jsonify({"error": "name and price are required"}), 400

    if data.get("category_id") and not Category.query.get(data["category_id"]):
        return jsonify({"error": "Invalid category_id"}), 400

    admin_id = get_jwt_identity()

    product = Product(
        name=name,
        description=data.get("description"),
        price=price,
        stock=data.get("stock", 0),
        image_url=data.get("image_url"),
        category_id=data.get("category_id"),
        created_by=admin_id,
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product created", "product": product_schema.dump(product)}), 201


@admin_bp.route("/products/<int:product_id>", methods=["PUT"])
@role_required("admin")
def update_product(product_id):
    """Admin edits an existing product's details (price, stock, etc)."""
    product = Product.query.get_or_404(product_id)
    data = request.get_json() or {}

    for field in ("name", "description", "price", "stock", "image_url", "category_id", "is_active"):
        if field in data:
            setattr(product, field, data[field])

    db.session.commit()
    return jsonify({"message": "Product updated", "product": product_schema.dump(product)}), 200

@admin_bp.route("/products/<int:product_id>", methods=["DELETE"])
@role_required("admin")
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_active = False
    db.session.commit()
    return jsonify({"message": "Product deactivated"}), 200


@admin_bp.route("/products", methods=["GET"])
@role_required("admin")
def list_all_products_for_admin():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return jsonify(products_schema.dump(products)), 200

# ---------------------------------------------------------------------
# ORDER MANAGEMENT
# ---------------------------------------------------------------------

@admin_bp.route("/orders", methods=["GET"])
@role_required("admin")
def list_orders():
    """Admin views every customer order so they know what needs fulfilling."""
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify(orders_schema.dump(orders)), 200


@admin_bp.route("/orders/<int:order_id>/status", methods=["PATCH"])
@role_required("admin")
def update_order_status(order_id):
    """Admin moves an order forward, e.g. pending -> shipped -> delivered."""
    order = Order.query.get_or_404(order_id)
    new_status = (request.get_json() or {}).get("status")

    valid_statuses = [OrderStatus.PENDING, OrderStatus.PAID, OrderStatus.SHIPPED,
                       OrderStatus.DELIVERED, OrderStatus.CANCELLED]
    if new_status not in valid_statuses:
        return jsonify({"error": f"status must be one of {valid_statuses}"}), 400

    order.status = new_status
    db.session.commit()
    return jsonify({"message": "Order status updated", "order": order_schema.dump(order)}), 200


# ---------------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------------

@admin_bp.route("/dashboard", methods=["GET"])
@role_required("admin")
def dashboard():
    total_products = Product.query.count()
    active_products = Product.query.filter_by(is_active=True).count()

    # Products with fewer than 5 left — a simple restock alert.
    low_stock_products = Product.query.filter(Product.stock < 5, Product.is_active == True).all()

    orders_by_status = dict(
        db.session.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    )
    total_orders = Order.query.count()

    return jsonify({
        "total_products": total_products,
        "active_products": active_products,
        "low_stock_products": products_schema.dump(low_stock_products),
        "total_orders": total_orders,
        "orders_by_status": orders_by_status,
    }), 200
