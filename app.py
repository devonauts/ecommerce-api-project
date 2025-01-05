
from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
import os
from config import Config
from config.settings import jwtConfig
from routes.users import users_bp
from routes.orders import orders_bp
from routes.products import products_bp
from flask_jwt_extended import JWTManager
from authentication.routes import auth_bp
from models import db  # Database from models/__init__.py

 
# Initialize Flask app
app = Flask(__name__)

# Load configuration from Config class
app.config.from_object(Config)

# Load jwtConfig explicitly
app.config.update(
    SECRET_KEY=jwtConfig.SECRET_KEY,
    JWT_SECRET_KEY=jwtConfig.JWT_SECRET_KEY,
    JWT_ALGORITHM=jwtConfig.JWT_ALGORITHM,
    JWT_ACCESS_TOKEN_EXPIRES=jwtConfig.JWT_ACCESS_TOKEN_EXPIRES,
)
# Initialize JWT Manager
jwt = JWTManager(app)

# Initialize extensions
db.init_app(app)  # Initialize SQLAlchemy
ma = Marshmallow(app)  # Initialize Marshmallow


# Ensure the upload folder exists
os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(users_bp, url_prefix='/api')  # All user routes prefixed with /api/users
app.register_blueprint(orders_bp, url_prefix='/api')  # Order routes prefixed with /api/orders
app.register_blueprint(products_bp, url_prefix='/api')  # Product routes prefixed with /api/products

# Error handling middleware
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Database initialization
with app.app_context():
    db.create_all()  # Create database tables

# Debugging: Verify the configuration
print(f"JWT_SECRET_KEY: {app.config.get('JWT_SECRET_KEY')}")
print(f"SECRET_KEY: {app.config.get('SECRET_KEY')}")
print(f"JWT_ALGORITHM: {app.config.get('JWT_ALGORITHM')}")
# Run the app
if __name__ == "__main__":
    app.run(debug=True)
 