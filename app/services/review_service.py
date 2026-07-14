from app.extensions import db
from app.models.review import Review

class ReviewService:
    @staticmethod
    def get_all_reviews():
        return Review.query.all()

    @staticmethod
    def get_review_by_id(review_id):
        return Review.query.get(review_id)
    
    @staticmethod
    def get_reviews_by_product_id(product_id):
        return Review.query.filter_by(product_id=product_id).all()
    
    @staticmethod
    def get_reviews_by_user_id(user_id):
        return Review.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_review(data):
        new_review = Review(**data)
        db.session.add(new_review)
        db.session.commit()
        return new_review

    @staticmethod
    def update_review(review, data):
        for key, value in data.items():
                setattr(review, key, value)
        db.session.commit()
        return review

    @staticmethod
    def delete_review(review):
            db.session.delete(review)
            db.session.commit()