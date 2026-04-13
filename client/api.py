import httpx
import os
from dotenv import load_dotenv
from uuid import UUID as Uuid

from client.token_storage import load_token


load_dotenv()

"""API interaction functions for user authentication and profile management."""


API_BASE_URL = os.getenv("API_BASE_URL")


def auth_headers():
    """Generate authorization headers using the stored token."""

    token_data = load_token()
    if not token_data or "access_token" not in token_data:
        raise ValueError("Missing authentication token. Please log in first.")
    return {"Authorization": f"Bearer {token_data['access_token']}"}


def get_my_profile():
    """Fetch the profile of the currently authenticated user."""
    response = httpx.get(url=f"{API_BASE_URL}/users/profile/me", headers=auth_headers())
    response.raise_for_status()

    profile = response.json()

    # Print user profile details
    for title, data in profile.items():
        print(f"{title}: {data}") 
    return profile


def get_messages(conversationId: str):

    response = httpx.get(
        url=f"{API_BASE_URL}/messages/{conversationId}", headers=auth_headers()
    )
    response.raise_for_status()
    return response.json()


def save_messages():

    response = httpx.get(
        url=f"{API_BASE_URL}/messages/save_message", headers=auth_headers()
    )
    return response.json()


def get_user_by_username(username: str) -> dict:
    """Fetch a user profile by username for recipient lookup."""
    response = httpx.get(
        url=f"{API_BASE_URL}/users/lookup/{username}",
        headers=auth_headers(),
    )
    response.raise_for_status()
    return response.json()


def get_websocket_url() -> str:
    """Build websocket chat URL with JWT query token."""
    token_data = load_token()
    if not token_data or "access_token" not in token_data:
        raise ValueError("Missing authentication token. Please log in first.")

    if API_BASE_URL.startswith("https://"):
        ws_base = API_BASE_URL.replace("https://", "wss://", 1)
    else:
        ws_base = API_BASE_URL.replace("http://", "ws://", 1)

    return f"{ws_base}/ws/chat?token={token_data['access_token']}"


def conversations():
    response = httpx.get(
        url=f"{API_BASE_URL}/conversations/get-conversations", headers=auth_headers()
    )
    response.raise_for_status()
    return response.json()


def get_user_by_id(userId: str) -> dict:
    response = httpx.get(
        url=f"{API_BASE_URL}/users/profile/{userId}", headers=auth_headers()
    )
    response.raise_for_status()
    return response.json()
