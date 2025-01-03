from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Custom Declarative Base
class Base(DeclarativeBase):
    pass

# SQLAlchemy instance using the custom base
db = SQLAlchemy(model_class=Base)

# Import models to ensure they are registered with SQLAlchemy
from .associations import order_product
from .user import User
from .order import Order
from .product import Product

__all__ = ['db', 'User', 'Order', 'Product', 'order_product']