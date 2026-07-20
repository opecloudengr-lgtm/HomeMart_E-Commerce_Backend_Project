from marshmallow import Schema, fields


class ChangeEmailSchema(Schema):
    email = fields.Email(required=True)


change_email_schema = ChangeEmailSchema()