from schemas import ma
from models.order import Order
from schemas.product_schema import ProductSchema
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

class OrderSchema(ma.SQLAlchemyAutoSchema):
    user_id = fields.Int(required=True, load_only=True)
    product_ids = fields.List(fields.Int(), load_only=True)
    class Meta:
            model = Order
            load_instance = True  # This ensures `load` creates a SQLAlchemy object
    
    id = auto_field(dump_only=True)  # Automatically mapped field
    order_date = auto_field(dump_only=True)  # Automatically set, read-only
    user_id = auto_field(required=True)  # Must be provided in the input
    status = fields.String()
    # Manually add the `products` relationship as a nested field
    products = fields.List(fields.Nested(ProductSchema), dump_only=True)

# Single Order Schema
order_schema = OrderSchema()

# Multiple Orders Schema
orders_schema = OrderSchema(many=True)
