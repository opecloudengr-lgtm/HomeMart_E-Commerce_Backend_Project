from app.extensions import db
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.inventory import Inventory

class CartService:

    @staticmethod
    def get_cart(user_id):

        cart = Cart.query.filter_by(
            user_id=user_id
        ).first()

        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()

        return {
            "success": True,
            "cart": cart
        }, 200

    @staticmethod
    def add_item(user_id, data):

        response, _ = CartService.get_cart(user_id)
        cart = response["cart"]

        product = db.session.get(Product, data["product_id"])

        if not product:
            return {
                "success": False,
                "message": "Product not found."
            }, 404

        inventory = Inventory.query.filter_by(
            product_id=product.id
        ).first()

        if not inventory:
            return {
                "success": False,
                "message": "Inventory not found."
            }, 404

        if inventory.quantity < data["quantity"]:
            return {
                "success": False,
                "message": "Insufficient stock."
            }, 400

        cart_item = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=product.id
        ).first()

        if cart_item:
            new_quantity = cart_item.quantity + data["quantity"]

            if new_quantity > inventory.quantity:
                return {
                    "success": False,
                    "message": "Insufficient stock."
                }, 400

            cart_item.quantity = new_quantity

        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product.id,
                quantity=data["quantity"]
            )
            db.session.add(cart_item)

        db.session.commit()

        return {
            "success": True,
            "message": "Item added to cart successfully.",
            "cart_item": cart_item
        }, 201

    @staticmethod
    def update_item(item_id, data):

        cart_item = db.session.get(CartItem, item_id)

        if not cart_item:
            return {
                "success": False,
                "message": "Cart item not found."
            }, 404

        quantity = data["quantity"]

        if quantity < 1:
            return {
                "success": False,
                "message": "Quantity must be at least 1."
            }, 400

        inventory = Inventory.query.filter_by(
            product_id=cart_item.product_id
        ).first()

        if not inventory:
            return {
                "success": False,
                "message": "Inventory not found."
            }, 404

        if quantity > inventory.quantity:
            return {
                "success": False,
                "message": "Insufficient stock."
            }, 400

        cart_item.quantity = quantity

        db.session.commit()

        return {
            "success": True,
            "message": "Cart item updated successfully.",
            "cart_item": cart_item
        }, 200