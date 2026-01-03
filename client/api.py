import httpx
import os
from dotenv import load_dotenv

from client.token_storage import load_token

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")


def auth_headers():
    """Generate authorization headers using the stored token."""

    token_data = load_token()
    return {"Authorization": f"Bearer {token_data["access_token"]}"}


def get_my_profile():

    response = httpx.get(url=f"{API_BASE_URL}/users/profile/me", headers=auth_headers())
    return response.json()


def get_messages():

    response = httpx.get(
        url=f"{API_BASE_URL}/messages/get_messages", headers=auth_headers()
    )
    return response.json()


def save_messages():

    response = httpx.get(
        url=f"{API_BASE_URL}/messages/save_message", headers=auth_headers()
    )
    return response.json()


def conversations():
    response = httpx.get(
        url=f"{API_BASE_URL}/conversations/get_conversations", headers=auth_headers()
    )
    return response.json()
