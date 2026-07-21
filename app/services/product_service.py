from sqlalchemy import or_
from app.extensions import db
from app.models.product import Product
from app.models.category import Category
from app.models.brand import Brand
from app.models.inventory import Inventory
from sqlalchemy.orm import joinedload, selectinload

class ProductService:
    @staticmethod
    def get_all(page=1, per_page=10, search=None, category_id=None, brand_id=None, sort="latest"):
        query = Product.query.filter_by(
        is_active=True
    )

        if search:
            query = query.filter(
            Product.name.ilike(
                f"%{search}%"
            )
        )

        if category_id:

            query = query.filter_by(
            category_id=category_id
        )

        if brand_id:

            query = query.filter_by(
            brand_id=brand_id
            )

        if sort == "price_asc":

            query = query.order_by(
            Product.price.asc()
            )

        elif sort == "price_desc":

            query = query.order_by(
            Product.price.desc()
            )

        elif sort == "name":

            query = query.order_by(
            Product.name.asc()
            )

        else:

            query = query.order_by(
            Product.created_at.desc()
            )

        pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
        )

        return {
        "success": True,
        "products": pagination.items,
        "page": pagination.page,
        "pages": pagination.pages,
        "total": pagination.total
        }, 200
    
    @staticmethod
    def get_by_id(product_id):

        product = (
        Product.query
        .options(
            joinedload(Product.category),
            joinedload(Product.brand),
            joinedload(Product.inventory),
            selectinload(Product.product_images),
            selectinload(Product.reviews)
        )
        .filter_by(
            id=product_id,
            is_active=True
        )
        .first()
        )

        if not product:
            return {
            "success": False,
            "message": "Product not found."
            }, 404

        return {
        "success": True,
        "product": product
        }, 200
    
    @staticmethod
    def create(data):

        category = db.session.get(Category, data["category_id"])

        if not category:
            return {
            "success": False,
            "message": "Category not found."
            }, 404

        if data.get("brand_id"):
            brand = db.session.get(Brand, data["brand_id"])

            if not brand:
                return {
                "success": False,
                "message": "Brand not found."
                }, 404

        existing = Product.query.filter_by(name=data["name"]).first()

        if existing:
            return {
            "success": False,
            "message": "Product already exists."
            }, 409

        product = Product(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        category_id=data["category_id"],
        brand_id=data.get("brand_id"),
        is_active=True
        )

        db.session.add(product)
        db.session.flush()

        inventory = Inventory(
        product_id=product.id,
        quantity=data.get("stock_quantity", 0)
        )

        db.session.add(inventory)
        db.session.commit()

        return {
        "success": True,
        "message": "Product created successfully.",
        "product": product
        }, 201
    
    @staticmethod
    def update(product_id, data):

        product = db.session.get(
        Product,
        product_id
        )

        if not product:
            return {
            "success": False,
            "message": "Product not found."
            }, 404

        if "category_id" in data:

            category = db.session.get(
            Category,
            data["category_id"]
            )

            if not category:
                return {
                "success": False,
                "message": "Category not found."
                }, 404

        if "brand_id" in data:

            if data["brand_id"] is not None:

                brand = db.session.get(
                Brand,
                data["brand_id"]
                )

                if not brand:
                    return {
                    "success": False,
                    "message": "Brand not found."
                    }, 404

        if "name" in data:

            existing = Product.query.filter(
            Product.name == data["name"],
            Product.id != product.id
            ).first()

            if existing:
                return {
                "success": False,
                "message": "A product with this name already exists."
                }, 409

        for key, value in data.items():
            setattr(product, key, value)

        db.session.commit()

        return {
        "success": True,
        "message": "Product updated successfully.",
        "product": product
        }, 200
    
    @staticmethod
    def update_status(product_id, is_active):

        product = db.session.get(
        Product,
        product_id
        )

        if not product:
         return {
            "success": False,
            "message": "Product not found."
            }, 404

        product.is_active = is_active

        db.session.commit()

        return {
        "success": True,
        "message": (
            "Product activated successfully."
            if is_active
            else
            "Product deactivated successfully."
        ),
        "product": product
        }, 200
    
    @staticmethod
    def delete(product_id):

        product = db.session.get(
        Product,
        product_id
        )

        if not product:
            return {
            "success": False,
            "message": "Product not found."
            }, 404

        if product.order_items:
            return {
            "success": False,
            "message": (
                "Cannot delete a product "
                "that has been ordered."
            )
            }, 400

        db.session.delete(product)

        db.session.commit()

        return {
        "success": True,
        "message": "Product deleted successfully."
        }, 200