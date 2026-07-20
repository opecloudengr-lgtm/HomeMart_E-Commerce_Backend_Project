from marshmallow import (Schema, ValidationError, fields, validates_schema, validate)


class ChangePasswordSchema(Schema):

    current_password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128)
    )

    new_password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128)
    )

    confirm_password = fields.String(
        required=True,
        load_only=True
    )

    @validates_schema
    def validate_passwords(self, data, **kwargs):

        if data["new_password"] != data["confirm_password"]:
            raise ValidationError(
                {
                    "confirm_password": [
                        "Passwords do not match."
                    ]
                }
                )


change_password_schema = ChangePasswordSchema()