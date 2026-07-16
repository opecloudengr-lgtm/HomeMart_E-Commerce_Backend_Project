from marshmallow import Schema, fields, validate, validates_schema, ValidationError

class RegisterSchema(Schema):
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.String(required=True, validate=validate.Length(min=6, max=128))
    confirm_password = fields.String(required=True, validate=validate.Length(min=6, max=128))

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        if data.get("password") != data.get("confirm_password"):
            raise ValidationError("Passwords must match.", field_name="confirm_password")

register_schema = RegisterSchema()