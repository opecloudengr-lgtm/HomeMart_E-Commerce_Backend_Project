from flask import Blueprint, request, jsonify
from app.models import Product, Category
from app.schemas import product_schema, products_schema, categories_schema

product_bp = Blueprint("products", __name__, url_prefix="/products")


@product_bp.route("", methods=["GET"])
def browse_products():
    query = Product.query.filter_by(is_active=True)

    category_id = request.args.get("category_id", type=int)
    if category_id:
        query = query.filter_by(category_id=category_id)

    search = request.args.get("search")
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    min_price = request.args.get("min_price", type=float)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    max_price = request.args.get("max_price", type=float)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.order_by(Product.created_at.desc()).all()
    return jsonify(products_schema.dump(products)), 200


@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.filter_by(id=product_id, is_active=True).first_or_404()
    return jsonify(product_schema.dump(product)), 200


@product_bp.route("/categories", methods=["GET"])
def list_categories():
    categories = Category.query.all()
    return jsonify(categories_schema.dump(categories)), 200
