from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

load_dotenv()

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


# JWT to be signed with this secret key using the HS256 algorithm
SECRET_KEY = os.get_env("SECRET_KEY")
ALGORITHM = "HS256"
# lifespan of access token in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_jwt_token(data: dict) -> str:
    """
        creating a JWT token for secure authentication and authorization
    Args:
        data (dict): data to be encoded in the token

    Returns:
        str: encoded JWT token
    
    Notes:
        - Token is signed using HS256 algorithm and SECRET_KEY.
        - Token expires after ACCESS_TOKEN_EXPIRE_MINUTES.
        - Include only necessary information for authentication; sensitive data should not be stored in the token.
        - Use this token in Bearer authentication headers for protected endpoints.

    """

    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire
    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_jwt_token(token: str) -> dict:
    """"
        Decodes a JWT token to retrieve userId
    Args:
        token(str): JWT token to be decoded

    """""
    try:
        decoded_jwt = jwt.decode(jwt=token, algorithms=ALGORITHM, key=SECRET_KEY)
    except ExpiredSignatureError:
        print("Token has expired")
        return None 
    except InvalidTokenError:
        print("Invalid Token")
        return None

    return decoded_jwt.get('userId')