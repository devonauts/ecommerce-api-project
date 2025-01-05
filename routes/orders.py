from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from models import db
from models.order import Order
from models.product import Product
from schemas.order_schema import order_schema, orders_schema
from datetime import datetime
from flask_jwt_extended import jwt_required
from flask import jsonify, request
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

# Create a new order
@orders_bp.route('/order', methods=['POST'])
@jwt_required()
def create_order():
    data = request.json
    try:
        # Validate and deserialize input data
        order = order_schema.load(data)
#    except ValidationError as e:
#        return jsonify(e.messages), 400
    except ValidationError as e:
        print(e.messages)  # Log validation errors
        return jsonify(e.messages), 400

    # Add products to the order if product_ids are provided
    product_ids = data.get('product_ids', [])
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
@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    orders = Order.query.all()
    return orders_schema.jsonify(orders), 200



# Get an order by ID
@orders_bp.route('/order/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return order_schema.jsonify(order), 200

# Update an order by ID
@orders_bp.route('/order/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.json

    try:
        # Validate and deserialize input data (partial=True allows partial updates)
        updated_data = order_schema.load(data, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Update order fields
    if 'order_date' in data:  # Check if order_date is in the payload
        order.order_date = updated_data.order_date
    if 'user_id' in data:  # Check if user_id is in the payload
        order.user_id = updated_data.user_id

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

    return order_schema.dump(order), 200


# Delete an order by ID
@orders_bp.route('/order/<int:order_id>', methods=['DELETE']) 
@jwt_required()
def delete_order(order_id): 
    order = Order.query.get_or_404(order_id)
    try:
        db.session.delete(order)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Error deleting order from the database"}), 500
    return jsonify({"message": "Order deleted successfully"}), 200

#Additional end-points for extra points or bonus
@orders_bp.route('/orders/filter', methods=['GET'])
@jwt_required()
def search_and_filter_orders():
    try:
        # Get query parameters from the request
        data = request.json
        user_id = data.get('user_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Validate and parse dates
        if start_date or end_date:
            try:
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        # Start building the query
        query = Order.query

        # Filter by user_id if provided
        if user_id:
            query = query.filter(Order.user_id == user_id)

        # Filter by date range if both start_date and end_date are provided
        if start_date and end_date:
            query = query.filter(Order.order_date.between(start_date, end_date))

        # Debugging Information
        print("User ID:", user_id)
        print("Start Date:", start_date)
        print("End Date:", end_date)

        # Execute the query and get results
        orders = query.all()
        print("Orders Fetched:", orders)

        # Check if any orders were found
        if not orders:
            return jsonify({"message": "No orders found matching the criteria"}), 404

        # Serialize the results and return them
        return jsonify(orders_schema.dump(orders)), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500
#bulk update for status of order
@orders_bp.route('/orders/bulk_status', methods=['PUT'])
#@jwt_required()
def bulk_update_order_status():
    # Get batch size and status from the request body
    data = request.json
    batch_size = data.get('batch_size')
    new_status = data.get('status')

    # Validate batch size
    if batch_size not in [1,2,5,10, 20, 50, 100, 500]:
        return jsonify({"error": "Invalid batch size. Choose from 1,2,5,10, 20, 50, 100, 500"}), 400

    # Validate new status
    if not new_status:
        return jsonify({"error": "Status is required"}), 400

    # Get the first `batch_size` orders
    orders = Order.query.limit(batch_size).all()

    # Update the status of each order
    for order in orders:
        order.status = new_status

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Error updating orders"}), 500

    return jsonify({"message": f"{len(orders)} orders updated to '{new_status}'"}), 200

