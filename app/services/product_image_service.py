from app.extensions import db
from app.models.product_image import ProductImage


class ProductImageService:

    @staticmethod
    def get_all():
        return ProductImage.query.all()

    @staticmethod
    def get_by_id(image_id):
        return ProductImage.query.get(image_id)

    @staticmethod
    def get_by_product(product_id):
        return ProductImage.query.filter_by(product_id=product_id).all()

    @staticmethod
    def create(data):
        image = ProductImage(**data)
        db.session.add(image)
        db.session.commit()
        return image

    @staticmethod
    def delete(image):
        db.session.delete(image)
        db.session.commit()