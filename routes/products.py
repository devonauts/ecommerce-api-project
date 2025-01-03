from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models import db
from models.product import Product
from sqlalchemy import select
from schemas.product_schema import product_schema

products_bp = Blueprint('products', __name__)

# Create a new product
@products_bp.route('/products', methods=['POST'])
def create_products():
    try:
        # Validate and deserialize input JSON
        product_data = product_schema.load(request.json)
        
    except ValidationError as e:
        return jsonify(e.messages), 400
    print(f'this is the print statement ------>>>>{product_data}')
    products = Product(name = product_data['name'], price = product_data['price'])
    db.session.add(products)
    db.session.commit()

    return product_schema.jsonify(products), 201


# Get all products
@products_bp.route('/products', methods=['GET'])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    if not products:
        return jsonify([]),200
    return product_schema.jsonify(products),200

# Get a product by ID
@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return product_schema.jsonify(product), 200

# Update a product by ID
@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.json

    try:
        # Validate input data (partial=True allows updating only specific fields)
        updated_data = product_schema.load(data, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Update product fields
    product.name = updated_data.get('name', product.name)
    product.price = updated_data.get('price', product.price)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return product_schema.jsonify(product), 200

# Delete a product by ID
@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Product deleted successfully"}), 200
