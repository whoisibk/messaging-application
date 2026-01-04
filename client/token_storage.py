from pathlib import Path
import json


# Path(__file__) is the location of token_storage.py
# .parent is the 'client' directory
TOKEN_PATH = Path(__file__).parent / "mytoken.json"

# TOKEN_PATH.touch(exist_ok=True)  # This physically creates the empty file NOW

def save_token(token_data: dict):
    """Saves the authentication token data to a file in JSON format."""
    TOKEN_PATH.write_text(json.dumps(token_data))


def load_token() -> dict | None:
    """Retrieve stored token data"""

    if TOKEN_PATH.exists() is None or TOKEN_PATH.is_file() is False:
        return None
    return json.loads(TOKEN_PATH.read_text())


def delete_token():
    """Deletes the stored token data file"""
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()
