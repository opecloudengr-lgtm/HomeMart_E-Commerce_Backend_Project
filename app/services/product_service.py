from sqlalchemy import or_
from app.extensions import db
from app.models.product import Product

class ProductService:
    @staticmethod
    def get_all_products():
        return Product.query.all()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def create_product(data):
        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def update_product(product, data):
        for key, value in data.items():
                setattr(product, key, value)
        db.session.commit()
        return product

    @staticmethod
    def delete_product(product):
            db.session.delete(product)
            db.session.commit()

    @staticmethod
    def search_products(keyword):
        return Product.query.filter(
            or_(
                Product.name.ilike(f'%{keyword}%'),
                Product.description.ilike(f'%{keyword}%')
            )
        ).all()
    
    @staticmethod
    def get_products_by_category(category_id):
        return Product.query.filter_by(category_id=category_id).all()
    
    @staticmethod
    def get_products_by_brand(brand_id):
        return Product.query.filter_by(brand_id=brand_id).all()
    
    @staticmethod
    def get_latest_products(limit=10):
        return Product.query.order_by(Product.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_featured_products():
        return Product.query.filter_by(is_featured=True).all()
    
    @staticmethod
    def get_active_products():
        return Product.query.filter_by(is_active=True).all()