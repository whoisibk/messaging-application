import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt for secure storage.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        str: The bcrypt hashed password as a UTF-8 string.
    """
    # Salt adds randomness so identical passwords produce different hashes.
    salt = bcrypt.gensalt()

    # Hash the password by combining it with the salt.
    # encode('utf-8') converts the string to bytes, as bcrypt expects bytes.
    # bcrypt.hashpw() returns bytes containing the salt + hash.
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

    # Decode the bytes back to a UTF-8 string for storage in a database.
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a stored bcrypt hashed password.

    Args:
        plain_password (str): The plaintext password to verify.
        hashed_password (str): The stored bcrypt hashed password.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    # bcrypt.checkpw() expects both arguments as bytes, so we encode them.
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
