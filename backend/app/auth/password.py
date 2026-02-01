"""Password hashing utilities."""
import hashlib
import secrets


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt."""
    salt = secrets.token_hex(16)
    pwdhash = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${pwdhash}"


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    try:
        salt, pwdhash = password_hash.split('$')
        return hashlib.sha256((salt + password).encode()).hexdigest() == pwdhash
    except:
        return False
