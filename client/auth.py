import httpx
import os
from dotenv import load_dotenv

from client.token_storage import save_token


load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")


def Login():

    userName= input("Username: ")
    password = input("Password: ")

    data  = {
        "userName": userName,
        "password": password
    }

    # Make a POST request (username and password) to the user login endpoint 
    response = httpx.post(url=f"{API_BASE_URL}/users/login", data=data)

    # Raise exception for HTTP Errors
    response.raise_for_status()

    # Convert response to JSON string
    token_data = response.json()

    # Save the token to a file
    save_token(token_data)
