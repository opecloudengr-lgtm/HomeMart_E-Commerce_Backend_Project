from app.extensions import db
from app.models.brand import Brand

class BrandService:
    @staticmethod
    def get_all_brands():
        return Brand.query.all()

    @staticmethod
    def get_brand_by_id(brand_id):
        return Brand.query.get(brand_id)

    @staticmethod
    def create_brand(data):
        new_brand = Brand(**data)
        db.session.add(new_brand)
        db.session.commit()
        return new_brand

    @staticmethod
    def update_brand(brand, data):
        for key, value in data.items():
                setattr(brand, key, value)
        db.session.commit()
        return brand

    @staticmethod
    def delete_brand(brand):
            db.session.delete(brand)
            db.session.commit()