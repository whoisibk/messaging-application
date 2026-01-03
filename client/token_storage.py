from pathlib import Path
import json


# File path (to exist in current working directory) to store the token data for the client 
TOKEN_PATH = Path.cwd() / "mytoken.json" 

def save_token(token_data: dict):
    """Saves the authentication token data to a file in JSON format."""    
    TOKEN_PATH.write_text(json.dumps(token_data))


def load_token()-> dict | None:
    """Retrieve stored token data"""

    if TOKEN_PATH.exists() is None:
        return None
    return json.loads(TOKEN_PATH.read_text())

def delete_token():
    """Deletes the stored token data file"""
    if TOKEN_PATH.exists():
        TOKEN_PATH.unlink()