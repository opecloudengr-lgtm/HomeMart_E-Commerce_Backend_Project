from app.extensions import db
from app.models.category import Category

class CategoryService:
    @staticmethod
    def get_all_categories():
        return Category.query.all()

    @staticmethod
    def get_category_by_id(category_id):
        return Category.query.get(category_id)

    @staticmethod
    def create_category(data):
        new_category = Category(**data)
        db.session.add(new_category)
        db.session.commit()
        return new_category

    @staticmethod
    def update_category(category, data):
        for key, value in data.items():
                setattr(category, key, value)
        db.session.commit()
        return category

    @staticmethod
    def delete_category(category):
            db.session.delete(category)
            db.session.commit()