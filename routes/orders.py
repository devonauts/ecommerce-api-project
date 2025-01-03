from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from models import db
from models.order import Order
from models.product import Product
from schemas.order_schema import order_schema, orders_schema

orders_bp = Blueprint('orders', __name__)

# Create a new order
@orders_bp.route('/', methods=['POST'])
def create_order():
    data = request.json
    try:
        # Validate input data
        order_data = order_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Create the Order instance
    order = Order(
        order_date=order_data['order_date'],
        user_id=order_data['user_id']
    )

    # Add products to the order if product_ids are provided
    product_ids = order_data.get('product_ids', [])
    for product_id in product_ids:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": f"Product with id {product_id} does not exist"}), 404
        order.products.append(product)

    try:
        db.session.add(order)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Error saving order to the database"}), 500

    return order_schema.jsonify(order), 201

# Get all orders
@orders_bp.route('/', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return orders_schema.jsonify(orders), 200

# Get an order by ID
@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return order_schema.jsonify(order), 200

# Update an order by ID
@orders_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.json

    try:
        # Validate input data (partial=True allows updating only specific fields)
        updated_data = order_schema.load(data, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Update order fields
    order.order_date = updated_data.get('order_date', order.order_date)
    order.user_id = updated_data.get('user_id', order.user_id)

    # Update products if product_ids are provided
    if 'product_ids' in data:
        order.products.clear()  # Remove existing products
        product_ids = data['product_ids']
        for product_id in product_ids:
            product = Product.query.get(product_id)
            if not product:
                return jsonify({"error": f"Product with id {product_id} does not exist"}), 404
            order.products.append(product)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Error updating order in the database"}), 500

    return order_schema.jsonify(order), 200

# Delete an order by ID
@orders_bp.route('/<int:order_id>', methods=['DELETE']) 

def delete_order(order_id): 
    order = Order.query.get_or_404(order_id)
    try:
        db.session.delete(order)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Error deleting order from the database"}), 500
    return jsonify({"message": "Order deleted successfully"}), 200
