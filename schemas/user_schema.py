from schemas import ma
from models.user import User
from marshmallow import fields, validate

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        email = fields.Email(required=True)
        username = fields.String(required=True, validate=validate.Length(min=3))
        password = fields.String(required=True, validate=validate.Length(min=6))
       # address = fields.String(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
