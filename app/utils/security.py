from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """Hash a password for storing."""
    return generate_password_hash(password)

def verify_password(password_hash, password):
    """Verify a pain text password against its hash."""
    return check_password_hash(password_hash, password)