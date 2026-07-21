from app.extensions import db
from app.models.category import Category

class CategoryService:
    @staticmethod
    def get_all(include_inactive=False):

        query = Category.query

        if not include_inactive:
            query = query.filter_by(is_active=True)

        categories = query.order_by(
        Category.name.asc()
        ).all()

        return {
        "success": True,
        "count": len(categories),
        "categories": categories
        }, 200

    @staticmethod
    def get_by_id(category_id):

        category = db.session.get(
        Category,
        category_id
        )

        if not category:
            return {
            "success": False,
            "message": "Category not found."
            }, 404

        return {
        "success": True,
        "category": category
        }, 200

    @staticmethod
    def create(data):

        existing = Category.query.filter_by(
        name=data["name"]
        ).first()

        if existing:
            return {
            "success": False,
            "message": "Category already exists."
            }, 409

        category = Category(**data)

        db.session.add(category)
        db.session.commit()

        return {
        "success": True,
        "message": "Category created successfully.",
        "category": category
        }, 201

    @staticmethod
    def update(category_id, data):

        category = db.session.get(
        Category,
        category_id
        )

        if not category:
            return {
            "success": False,
            "message": "Category not found."
            }, 404

        if "name" in data:

            existing = Category.query.filter(
            Category.name == data["name"],
            Category.id != category_id
            ).first()

            if existing:
                return {
                "success": False,
                "message": "Category already exists."
                }, 409

        for key, value in data.items():
            setattr(category, key, value)

        db.session.commit()

        return {
        "success": True,
        "message": "Category updated successfully.",
        "category": category
        }, 200

    @staticmethod
    def activate(category_id):

        category = db.session.get(
        Category,
        category_id
        )

        if not category:
            return {
            "success": False,
            "message": "Category not found."
            }, 404

        category.is_active = True

        db.session.commit()

        return {
        "success": True,
        "message": "Category activated successfully."
        }, 200
    
    @staticmethod
    def deactivate(category_id):

        category = db.session.get(
        Category,
        category_id
        )

        if not category:
            return {
            "success": False,
            "message": "Category not found."
            }, 404

        category.is_active = False

        db.session.commit()

        return {
        "success": True,
        "message": "Category deactivated successfully."
        }, 200
    
    @staticmethod
    def delete(category_id):

        category = db.session.get(
        Category,
        category_id
        )

        if not category:
            return {
            "success": False,
            "message": "Category not found."
            }, 404

        if category.products:
            return {
            "success": False,
            "message": (
                "Cannot delete a category "
                "that contains products."
                )
            }, 400

        db.session.delete(category)

        db.session.commit()

        return {
        "success": True,
        "message": "Category deleted successfully."
        }, 200