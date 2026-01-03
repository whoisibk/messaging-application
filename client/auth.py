import httpx
import os
from dotenv import load_dotenv

from client.token_storage import save_token, load_token, delete_token
from app.utils.auth import decode_jwt_token


load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")


def Login():
    """Logs user in with username and password and saves token to a file."""

    userName = input("Username: ")
    password = input("Password: ")

    data = {"userName": userName, "password": password}

    # Make a POST request (username and password) to the user login endpoint
    response = httpx.post(url=f"{API_BASE_URL}/users/login", data=data)

    # Raise exception for HTTP Errors
    response.raise_for_status()

    # Convert response to JSON string
    token_data = response.json()

    # Save the token to a file
    save_token(token_data)

    username = decode_jwt_token(load_token().get("access_token"))

    return f"Logged in as {userName}"


def Logout():
    """Logs out user by deleting the stored token."""
    delete_token()

    return "Logged out successfully"
