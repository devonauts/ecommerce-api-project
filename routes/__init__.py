from flask import Blueprint
from routes.users import users_bp
from routes.files import files_bp

def register_routes(app):
    #app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(orders_bp)  # Order routes prefixed with /api/orders
    app.register_blueprint(products_bp)  # Product routes prefixed with /api/products  
    app.register_blueprint(users_bp)  # All user routes prefixed with /api/users


 
    app.register_blueprint(files_bp)
