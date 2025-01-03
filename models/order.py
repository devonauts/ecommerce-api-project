from models import db
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Order(db.Model):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_date: Mapped[str] = mapped_column(db.DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Many-to-One Relationship with User
    
    user: Mapped["User"] = relationship('User', back_populates='orders')

    # Many-to-Many Relationship with Products
    products: Mapped[List["Product"]] = relationship('Product', secondary='order_product', back_populates='orders')
