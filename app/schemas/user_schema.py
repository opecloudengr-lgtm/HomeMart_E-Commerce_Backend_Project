from marshmallow import fields, Schema, validate
from app.extensions import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

    id = fields.String(dump_only=True)
    password_hash = fields.String(load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)

class UpdateUserSchema(Schema):
    first_name = fields.String(validate=validate.Length(min=2, max=50))
    last_name = fields.String(validate=validate.Length(min=2, max=50))
    phone = fields.String(validate=validate.Length(min=10, max=20))

user_schema = UserSchema()
users_schema = UserSchema(many=True)
update_user_schema = UpdateUserSchema()