from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity

def get_current_user_id():
    return get_jwt_identity()

def generate_access_tokens(identity):
    """Generate a JWT access token."""
    return create_access_token(identity=identity)

def generate_refresh_tokens(identity):
    """Generate a JWT refresh token."""
    return create_refresh_token(identity=identity)