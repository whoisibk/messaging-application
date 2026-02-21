import httpx
import os
from dotenv import load_dotenv

from client.token_storage import save_token, load_token, delete_token
from app.utils.auth import decode_jwt_token


load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")


def Login():
    """Logs user in with username and password and saves token to a file."""

    username = input("Username: ")
    password = input("Password: ")

    data = {"username": username, "password": password}

    try:
        # Make a POST request (username and password) to the user login endpoint
        response = httpx.post(url=f"{API_BASE_URL}/users/login", data=data)

        # Raise exception for HTTP Errors
        response.raise_for_status()

        # Convert response to JSON string
        token_data = response.json()

        # Save the token to a file
        save_token(token_data)

        # username = decode_jwt_token(load_token().get("access_token"))

        return username
    except httpx.HTTPStatusError as e:
        raise Exception(f"Login failed: {e.response.status_code} - {e.response.text}")
    
    except httpx.RequestError as e:
        raise Exception(f"Network or connection error during login: {str(e)}")
    
    except ValueError as e: 
        raise Exception(f"Failed to parse server response during login: {str(e)}")
    
    except OSError as e:
        raise Exception(f"Failed to save authentication token: {str(e)}")
    
    except Exception as e:
        raise Exception(f"An unexpected error occurred during login: {str(e)}")
    

def Logout():
    """Logs out user by deleting the stored token."""
    delete_token()

    return "Logged out successfully"


def SignUp():
    """Signs a new user up and makes a POST request"""
    firstName = input("First Name: ").strip()
    lastName = input("Last Name: ").strip()

    userName = input("Type in preferred username: ").strip()
    userEmail = input("Type in your email address: ").strip()

    password = input("Create a password: ")

    payload = {
            "firstName": firstName.title(),
            "lastName": lastName.title(),
            "userName": userName,
            "userEmail": userEmail.lower(),
            "password": password
    }

    response = httpx.post(f"{API_BASE_URL}/users/signup", json=payload)

    return f"\n\t\t\tSigned Up Successfully\nProceed to Login: "
