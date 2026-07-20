from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from app.schemas import (
    brand_schema,
    brands_schema,
)

from app.services.brand_service import BrandService

from app.utils.decorators import (
    admin_required,
    super_admin_required,
)

brand_bp = Blueprint(
    "brands",
    __name__,
    url_prefix="/brands"
)

@brand_bp.get("/")
def get_brands():

    response, status = BrandService.get_all()

    response["brands"] = brands_schema.dump(
        response["brands"]
    )

    return jsonify(response), status

@brand_bp.get("/<string:brand_id>")
def get_brand(brand_id):

    response, status = BrandService.get_by_id(
        brand_id
    )

    if response["success"]:
        response["brand"] = brand_schema.dump(
            response["brand"]
        )

    return jsonify(response), status

@brand_bp.post("/")
@admin_required
def create_brand():

    try:
        data = brand_schema.load(
            request.get_json()
        )

    except ValidationError as err:
        return jsonify(
            {
                "success": False,
                "errors": err.messages
            }
        ), 400

    response, status = BrandService.create(data)

    if response["success"]:
        response["brand"] = brand_schema.dump(
            response["brand"]
        )

    return jsonify(response), status

@brand_bp.put("/<int:brand_id>")
@admin_required
def update_brand(brand_id):

    try:
        data = brand_schema.load(
            request.get_json(),
            partial=True
        )

    except ValidationError as err:
        return jsonify(
            {
                "success": False,
                "errors": err.messages
            }
        ), 400

    response, status = BrandService.update(
        brand_id,
        data
    )

    if response["success"]:
        response["brand"] = brand_schema.dump(
            response["brand"]
        )

    return jsonify(response), status

@brand_bp.delete("/<int:brand_id>")
@super_admin_required
def delete_brand(brand_id):

    response, status = BrandService.delete(
        brand_id
    )

    return jsonify(response), status