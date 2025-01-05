from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import db
from typing import List
from sqlalchemy import Enum

class Order(db.Model):
    __tablename__ = 'orders'

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Automatically set the order_date to the current datetime
    order_date: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Foreign Key
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)

        # New status field
    status: Mapped[str] = mapped_column(db.Enum('Pending', 'Processing', 'Completed', 'Cancelled', name='order_status'),nullable=False,default='Pending')
    
    # Relationships
    user: Mapped["User"] = relationship('User', back_populates='orders')
    products: Mapped[List["Product"]] = relationship('Product', secondary='order_product', back_populates='orders')
