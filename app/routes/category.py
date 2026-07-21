from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from app.schemas import (
    category_schema,
    categories_schema
)

from app.services.category_service import CategoryService

from app.utils.decorators import (
    admin_required,
    super_admin_required
)

category_bp = Blueprint(
    "categories",
    __name__,
    url_prefix="/categories"
)

@category_bp.get("/")
def get_categories():

    response, status = CategoryService.get_all()

    response["categories"] = categories_schema.dump(
        response["categories"]
    )

    return jsonify(response), status

@category_bp.get("/<string:category_id>")
def get_category(category_id):

    response, status = CategoryService.get_by_id(
        category_id
    )

    if response["success"]:
        response["category"] = category_schema.dump(
            response["category"]
        )

    return jsonify(response), status

@category_bp.post("/")
@admin_required
def create_category():

    try:

        data = category_schema.load(
            request.get_json()
        )

    except ValidationError as err:

        return jsonify({
            "success": False,
            "errors": err.messages
        }), 400

    response, status = CategoryService.create(data)

    if response["success"]:
        response["category"] = category_schema.dump(
            response["category"]
        )

    return jsonify(response), status

@category_bp.put("/<string:category_id>")
@admin_required
def update_category(category_id):

    try:

        data = category_schema.load(
            request.get_json(),
            partial=True
        )

    except ValidationError as err:

        return jsonify({
            "success": False,
            "errors": err.messages
        }), 400

    response, status = CategoryService.update(
        category_id,
        data
    )

    if response["success"]:
        response["category"] = category_schema.dump(
            response["category"]
        )

    return jsonify(response), status

@category_bp.patch("/<string:category_id>/activate")
@admin_required
def activate_category(category_id):

    response, status = CategoryService.activate(
        category_id
    )

    return jsonify(response), status

@category_bp.patch("/<string:category_id>/deactivate")
@admin_required
def deactivate_category(category_id):

    response, status = CategoryService.deactivate(
        category_id
    )

    return jsonify(response), status

@category_bp.delete("/<string:category_id>")
@super_admin_required
def delete_category(category_id):

    response, status = CategoryService.delete(
        category_id
    )

    return jsonify(response), status