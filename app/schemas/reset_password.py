from marshmallow import (Schema, fields, validate, validates_schema, ValidationError)


class ResetPasswordSchema(Schema):

    token = fields.String(required=True)

    password = fields.String(required=True, load_only=True, validate=validate.Length(min=8, max=128))

    confirm_password = fields.String(required=True, load_only=True)

    @validates_schema
    def validate_passwords(self, data, **kwargs):

        if data["password"] != data["confirm_password"]:
            raise ValidationError({"comfirm_password": ["Passwords do not match."]})

reset_password_schema = ResetPasswordSchema()