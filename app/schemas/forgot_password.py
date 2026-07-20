from marshmallow import Schema, fields


class ForgotPasswordSchema(Schema):

    email = fields.Email(required=True)
forgot_password_schema = ForgotPasswordSchema()