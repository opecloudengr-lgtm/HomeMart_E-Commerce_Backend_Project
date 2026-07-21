from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.schemas import (
    product_schema,
    products_schema,
)

from app.services.product_service import ProductService

from app.utils.decorators import (
    admin_required,
    super_admin_required
)

product_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products"
)

@product_bp.get("/")
def get_products():

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    per_page = request.args.get(
        "per_page",
        default=10,
        type=int
    )

    search = request.args.get("search")

    category_id = request.args.get(
        "category_id",
        type=int
    )

    brand_id = request.args.get(
        "brand_id",
        type=int
    )

    sort = request.args.get(
        "sort",
        default="latest"
    )

    response, status = ProductService.get_all(
        page=page,
        per_page=per_page,
        search=search,
        category_id=category_id,
        brand_id=brand_id,
        sort=sort
    )

    response["products"] = products_schema.dump(
        response["products"]
    )

    return jsonify(response), status

@product_bp.get("/<string:product_id>")
def get_product(product_id):

    response, status = ProductService.get_by_id(
        product_id
    )

    if response["success"]:

        response["product"] = product_schema.dump(
            response["product"]
        )

    return jsonify(response), status

@product_bp.post("/")
@admin_required
def create_product():

    try:

        data = product_schema.load(
            request.get_json()
        )

    except ValidationError as err:

        return jsonify({
            "success": False,
            "errors": err.messages
        }), 400

    response, status = ProductService.create(
        data
    )

    if response["success"]:

        response["product"] = product_schema.dump(
            response["product"]
        )

    return jsonify(response), status

@product_bp.patch("/<string:product_id>")
@admin_required
def update_product(product_id):

    try:

        data = product_schema.load(
            request.get_json(),
            partial=True
        )

    except ValidationError as err:

        return jsonify({
            "success": False,
            "errors": err.messages
        }), 400

    response, status = ProductService.update(
        product_id,
        data
    )

    if response["success"]:

        response["product"] = product_schema.dump(
            response["product"]
        )

    return jsonify(response), status

@product_bp.patch("/<string:product_id>/activate")
@admin_required
def activate_product(product_id):

    response, status = ProductService.update_status(
        product_id,
        True
    )

    if response["success"]:

        response["product"] = product_schema.dump(
            response["product"]
        )

    return jsonify(response), status

@product_bp.patch("/<string:product_id>/deactivate")
@admin_required
def deactivate_product(product_id):

    response, status = ProductService.update_status(
        product_id,
        False
    )

    if response["success"]:

        response["product"] = product_schema.dump(
            response["product"]
        )

    return jsonify(response), status

@product_bp.delete("/<string:product_id>")
@super_admin_required
def delete_product(product_id):

    response, status = ProductService.delete(
        product_id
    )

    return jsonify(response), status