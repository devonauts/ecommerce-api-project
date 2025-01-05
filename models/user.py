from models import db
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String(50), nullable=False)
    username : Mapped[str] = mapped_column(db.String(80), nullable=False, unique=True)
    password : Mapped[str] = mapped_column(db.String(200), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), unique=True, nullable=False)
    address: Mapped[str] = mapped_column(db.String(255), nullable=True)

# for authentication purposes, we needed to add this 2 methods to set password and and to check password.
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # One-to-Many Relationship with Orders
    orders: Mapped[List["Order"]] = relationship('Order', back_populates='user', cascade='all, delete-orphan')

