import os
import secrets

class jwtConfig:
    # Generate a single secure random key
    _secret_key = secrets.token_hex(32)
    
    SECRET_KEY = os.getenv("SECRET_KEY", _secret_key)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", _secret_key)
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Expire after 1 hour
