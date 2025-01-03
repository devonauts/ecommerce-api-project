from models import db
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.order import Order
class Product(db.Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    # Many-to-Many Relationship with Orders
    orders: Mapped[List["Order"]] = relationship('Order',secondary='order_product',back_populates='products')

