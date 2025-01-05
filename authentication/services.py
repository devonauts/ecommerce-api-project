from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models.user import User
import json

def authenticate_user(username, password):
    """
    Authenticate the user based on username and password.
    """
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


def generate_access_token(user):
    """
    Generate a JWT token for the authenticated user using HS256.
    """
    # Convert user data to a JSON string for the identity
    identity = json.dumps({"id": user.id, "username": user.username})
    return create_access_token(identity=identity)