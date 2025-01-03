from models import db

# Many-to-Many Association Table for Orders and Products
order_product = db.Table(
    'order_product',  # Table name
    db.metadata,  # Use the metadata from SQLAlchemy for table creation
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id', ondelete="CASCADE"), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id', ondelete="CASCADE"), primary_key=True)
)
