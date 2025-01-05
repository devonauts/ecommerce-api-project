from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models import db
from models.product import Product
from sqlalchemy import select
from schemas.product_schema import product_schema
from schemas.product_schema import products_schema
from flask_jwt_extended import jwt_required



products_bp = Blueprint('products', __name__)

# Create a new product
@products_bp.route('/products', methods=['POST'])
@jwt_required()
def create_products():
    try:
        # Validate and deserialize input JSON
        product_data = product_schema.load(request.json)
        
    except ValidationError as e:
        return jsonify(e.messages), 400
    #print(f'this is the print statement ------>>>>{product_data}')
    products = Product(name = product_data['name'], price = product_data['price'])
    db.session.add(products)
    db.session.commit()

    return product_schema.jsonify(products), 201


# Get all products
@products_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    if not products:
        return jsonify([]),200
    return products_schema.jsonify(products),200

# Get a product by ID
@products_bp.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return product_schema.jsonify(product), 200

# Update a product by ID
@products_bp.route('/product/<int:product_id>', methods=['PUT'])
@jwt_required()
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
@products_bp.route('/product/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Product deleted successfully"}), 200


#pagination added for number of products
import logging

logging.basicConfig(level=logging.INFO)

@products_bp.route('/products/pagination', methods=['GET'])
#@jwt_required()
def get_paginated_products():
    try:
        # Log the raw JSON payload or query parameters
        logging.info("Request JSON: %s", request.json)
        logging.info("Request args: %s", request.args.to_dict())

        # Get pagination parameters from JSON payload
        data = request.json or {}
        page = data.get('pagination', request.args.get('pagination', 1, type=int))
        size = data.get('size', request.args.get('size', 10, type=int))

        # Validate parameters
        if not isinstance(page, int) or not isinstance(size, int) or page < 1 or size < 1:
            return jsonify({"error": "Page and size must be positive integers"}), 400

        logging.info("Pagination: page=%s, size=%s", page, size)

        # Apply pagination
        paginated_products = Product.query.paginate(page=page, per_page=size, error_out=False)

        # Log the paginated products
        logging.info("Paginated products: %s", [p.id for p in paginated_products.items])

        # Check for out-of-range pages
        if not paginated_products.items:
            return jsonify({"error": "Page out of range"}), 404

        # Serialize results
        products = [product_schema.dump(p) for p in paginated_products.items]

        return jsonify({
            "page": paginated_products.page,
            "per_page": paginated_products.per_page,
            "total": paginated_products.total,
            "pages": paginated_products.pages,
            "data": products
        }), 200

    except Exception as e:
        logging.error("Error: %s", str(e))
        return jsonify({"error": str(e)}), 500

