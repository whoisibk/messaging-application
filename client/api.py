import httpx
import os
from dotenv import load_dotenv

from client.token_storage import load_token
from app.services.user_ops import get_userId_by_userName


load_dotenv()

"""API interaction functions for user authentication and profile management."""


API_BASE_URL = os.getenv("API_BASE_URL")


def auth_headers():
    """Generate authorization headers using the stored token."""

    token_data = load_token()
    return {"Authorization": f"Bearer {token_data["access_token"]}"}


def get_my_profile():
    """Fetch the profile of the currently authenticated user."""
    response = httpx.get(url=f"{API_BASE_URL}/users/profile/me", headers=auth_headers())
    
    response.raise_for_status()

    # Print user profile details
    for title, data in response.json().items():
        print(f"{title}: {data}") 


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


def send_message():
    """Send a message to a specified recipient."""

    recipient = input("Enter recipient username: ").strip()
    message = input("Enter your message: ").strip()
    
    recipientId = get_userId_by_userName(recipient)

    data = {
        # UUIDs need to be converted to strings for JSON serialization
        "recipientId": str(recipientId),
        "message": message,
    }

    response = httpx.post(f"{API_BASE_URL}/ws/chat", json=data, headers=auth_headers())
    print(response)


def conversations():
    response = httpx.get(
        url=f"{API_BASE_URL}/conversations/get_conversations", headers=auth_headers()
    )
    return response.json()
