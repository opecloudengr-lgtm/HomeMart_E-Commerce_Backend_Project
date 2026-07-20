from marshmallow import Schema, fields, validate


class UpdateProfileSchema(Schema):

    first_name = fields.String(
        required=False,
        validate=validate.Length(min=2, max=100)
    )

    last_name = fields.String(
        required=False,
        validate=validate.Length(min=2, max=100)
    )

    phone = fields.String(
        required=False,
        validate=validate.Length(min=11, max=15)
    )


update_profile_schema = UpdateProfileSchema()