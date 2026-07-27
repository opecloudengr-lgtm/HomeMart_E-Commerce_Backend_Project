from app.extensions import ma
from app.models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = False
      
        fields = ("id", "name", "email", "role", "is_active", "created_at")

user_schema = UserSchema()
users_schema = UserSchema(many=True)