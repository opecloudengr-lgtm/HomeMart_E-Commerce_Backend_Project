from app.extensions import db
from app.models.brand import Brand

class BrandService:

    @staticmethod
    def get_all():

        brands = Brand.query.order_by(
            Brand.created_at.desc()
        ).all()

        return {
            "success": True,
            "count": len(brands),
            "brands": brands
        }, 200

    @staticmethod
    def get_by_id(brand_id):

        brand = db.session.get(
            Brand,
            brand_id
        )

        if not brand:
            return {
                "success": False,
                "message": "Brand not found."
            }, 404

        return {
            "success": True,
            "brand": brand
        }, 200

    @staticmethod
    def create(data):

        existing_brand = Brand.query.filter_by(
            name=data["name"]
        ).first()

        if existing_brand:
            return {
                "success": False,
                "message": "Brand already exists."
            }, 409

        brand = Brand(**data)

        db.session.add(brand)
        db.session.commit()

        return {
            "success": True,
            "message": "Brand created successfully.",
            "brand": brand
        }, 201

    @staticmethod
    def update(brand_id, data):

        brand = db.session.get(
            Brand,
            brand_id
        )

        if not brand:
            return {
                "success": False,
                "message": "Brand not found."
            }, 404

        if "name" in data:

            existing_brand = Brand.query.filter(
                Brand.name == data["name"],
                Brand.id != brand_id
            ).first()

            if existing_brand:
                return {
                    "success": False,
                    "message": "Brand already exists."
                }, 409

        for key, value in data.items():
            setattr(brand, key, value)

        db.session.commit()

        return {
            "success": True,
            "message": "Brand updated successfully.",
            "brand": brand
        }, 200

    @staticmethod
    def delete(brand_id):

        brand = db.session.get(
            Brand,
            brand_id
        )

        if not brand:
            return {
                "success": False,
                "message": "Brand not found."
            }, 404

        db.session.delete(brand)
        db.session.commit()

        return {
            "success": True,
            "message": "Brand deleted successfully."
        }, 200