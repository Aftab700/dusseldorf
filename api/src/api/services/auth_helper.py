import secrets

import bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    Bcrypt hashes include the salt, so we just need the plain text and the stored hash.
    """
    try:
        password_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Generate a bcrypt hash for a password.
    Note: Bcrypt has a maximum password length of 72 bytes.
    """
    # If the password is longer than 72 chars, bcrypt will truncate it.
    # We encode to bytes first as required by the bcrypt library.
    password_bytes = password.encode("utf-8")

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Return as a string for storage in MongoDB
    return hashed.decode("utf-8")


def generate_opaque_token() -> str:
    """Generate a secure, random opaque session token"""
    return secrets.token_urlsafe(32)
