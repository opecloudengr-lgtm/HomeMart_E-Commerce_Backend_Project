from flask import Blueprint, jsonify, request

from marshmallow import ValidationError

from flask_jwt_extended import jwt_required

from app.schemas import (
    cart_schema,
    cart_item_schema,
)

from app.services.cart_service import CartService

from app.utils.token import get_current_user_id

cart_bp = Blueprint(
    "cart",
    __name__,
    url_prefix="/cart"
)

@cart_bp.get("/")
@jwt_required()
def get_cart():

    user_id = get_current_user_id()

    response, status = CartService.get_cart(user_id)

    if response["success"]:
        response["cart"] = cart_schema.dump(
            response["cart"]
        )

    return jsonify(response), status

@cart_bp.post("/items")
@jwt_required()
def add_item():

    try:

        data = cart_item_schema.load(
            request.get_json()
        )

    except ValidationError as err:

        return jsonify({
            "success": False,
            "errors": err.messages
        }), 400

    user_id = get_current_user_id()

    response, status = CartService.add_item(
        user_id,
        data
    )

    return jsonify(response), status

@cart_bp.delete("/items/<int:item_id>")
@jwt_required()
def remove_item(item_id):

        response, status = CartService.remove_item(
        item_id
    )

        return jsonify(response), status

@cart_bp.get("/summary")
@jwt_required()
def cart_summary():

    user_id = get_current_user_id()

    response, status = CartService.cart_summary(
        user_id
    )

    return jsonify(response), status