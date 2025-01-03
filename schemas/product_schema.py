from schemas import ma
from models.product import Product
from marshmallow_sqlalchemy import auto_field

class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Product
        load_instance = True  # This ensures `load` creates a SQLAlchemy object

    name = auto_field()
    price = auto_field()

# Instantiate the schema
product_schema = ProductSchema()

# Multiple Products Schema
products_schema = ProductSchema(many=True)
