from flask import Blueprint, request, jsonify

from marshmallow import ValidationError
from sqlalchemy import select
from models import db
from models.user import User
from schemas.user_schema import user_schema, users_schema
from flask_jwt_extended import jwt_required


users_bp = Blueprint('users', __name__)

# Endpoint: Create a new user
@users_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    try:
        # Validate and deserialize input JSON
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Create and save the new user
    new_user = User(name=user_data['name'], email=user_data['email'], address=user_data.get('address'))
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

# Endpoint: Get all users
@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    if not users:
        return jsonify([]), 200
    return users_schema.jsonify(users), 200




# Endpoint: Get a user by ID
@users_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user), 200

# Endpoint: Update a user by ID
@users_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get_or_404(id)
    try:
        # Validate and deserialize input JSON
        user_data = user_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Update user fields
    user.name = user_data.get('name', user.name)
    user.email = user_data.get('email', user.email)
    user.address = user_data.get('address', user.address)
    user.username = user_data.get('username', user.username)
    db.session.commit()

    return user_schema.jsonify(user), 200

# Endpoint: Delete a user by ID
@users_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
