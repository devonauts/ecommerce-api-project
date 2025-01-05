from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from authentication import auth_bp
from authentication.services import authenticate_user, generate_access_token
from models import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import json


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    email = data.get('email')
    address = data.get('address')

    # Validate input
    if not username or not password or not email:
        return jsonify({"error": "Username, password, and email are required"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long"}), 400

    # Check if username or email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

   # if User.query.filter_by(email=email).first():
   #     return jsonify({"error": "Email already exists"}), 400

    # Create new user
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(
        username=username,
        password=hashed_password,
        name=name,
        email=email,
        address=address
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating user", "details": str(e)}), 500


# Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Authenticate user
    user = authenticate_user(username, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT token
    access_token = generate_access_token(user)
    return jsonify({"access_token": access_token}), 200

# Protected Route
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    # Parse the JSON string back into a dictionary
    current_user = json.loads(get_jwt_identity())
    return jsonify({"id": current_user["id"], "username": current_user["username"]}), 200