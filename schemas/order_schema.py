from schemas import ma
from models.order import Order
class OrderSchema(ma.SQLAlchemyAutoSchema):
        class Meta:
            model = Order

# Single Order Schema
order_schema = OrderSchema()

# Multiple Orders Schema
orders_schema = OrderSchema(many=True)
