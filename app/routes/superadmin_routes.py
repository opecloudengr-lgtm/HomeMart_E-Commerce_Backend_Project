from flask import Blueprint, request, jsonify
from sqlalchemy import func

from app.extensions import db
from app.models import User, Role, Category, Product, Order, OrderStatus, Payment, PaymentStatus
from app.schemas import user_schema, users_schema, category_schema, categories_schema
from app.utils.decorators import role_required

superadmin_bp = Blueprint("superadmin", __name__, url_prefix="/superadmin")


# ---------------------------------------------------------------------
# ADMIN MANAGEMENT
# ---------------------------------------------------------------------

@superadmin_bp.route("/admins", methods=["POST"])
@role_required("super_admin")
def create_admin():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists"}), 409

    admin = User(name=name, email=email, role=Role.ADMIN)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()

    return jsonify({"message": "Admin created successfully", "admin": user_schema.dump(admin)}), 201


@superadmin_bp.route("/admins", methods=["GET"])
@role_required("super_admin")
def list_admins():
    admins = User.query.filter_by(role=Role.ADMIN).all()
    return jsonify(users_schema.dump(admins)), 200


@superadmin_bp.route("/admins/<int:admin_id>/toggle-active", methods=["PATCH"])
@role_required("super_admin")
def toggle_admin_active(admin_id):
    admin = User.query.filter_by(id=admin_id, role=Role.ADMIN).first_or_404()
    admin.is_active = not admin.is_active
    db.session.commit()
    return jsonify({"message": "Admin status updated", "admin": user_schema.dump(admin)}), 200


@superadmin_bp.route("/users", methods=["GET"])
@role_required("super_admin")
def list_all_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200


# ---------------------------------------------------------------------
# CATEGORY MANAGEMENT
# ---------------------------------------------------------------------

@superadmin_bp.route("/categories", methods=["POST"])
@role_required("super_admin")
def create_category():
    data = request.get_json() or {}
    name = data.get("name")

    if not name:
        return jsonify({"error": "Category name is required"}), 400
    if Category.query.filter_by(name=name).first():
        return jsonify({"error": "Category already exists"}), 409

    category = Category(name=name, description=data.get("description"))
    db.session.add(category)
    db.session.commit()
    return jsonify(category_schema.dump(category)), 201


@superadmin_bp.route("/categories/<int:category_id>", methods=["DELETE"])
@role_required("super_admin")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200


# ---------------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------------

@superadmin_bp.route("/dashboard", methods=["GET"])
@role_required("super_admin")
def dashboard():
    total_customers = User.query.filter_by(role=Role.CUSTOMER).count()
    total_admins = User.query.filter_by(role=Role.ADMIN).count()
    total_products = Product.query.count()
    total_orders = Order.query.count()

    # Sum of amount for successfully completed payments = real revenue.
    total_revenue = (
        db.session.query(func.coalesce(func.sum(Payment.amount), 0))
        .filter(Payment.status == PaymentStatus.SUCCESS)
        .scalar()
    )

    orders_by_status = dict(
        db.session.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    )

    return jsonify({
        "total_customers": total_customers,
        "total_admins": total_admins,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "orders_by_status": orders_by_status,
    }), 200
