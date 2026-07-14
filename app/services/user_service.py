from app.extensions import db
from app.models.user import User

class UserService:
    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(data):
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user, data):
        for key, value in data.items():
                setattr(user, key, value)
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user):
            db.session.delete(user)
            db.session.commit()