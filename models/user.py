from models import db
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(50), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(db.String(255), nullable=True)

    # One-to-Many Relationship with Orders
    orders: Mapped[List["Order"]] = relationship('Order', back_populates='user', cascade='all, delete-orphan')
