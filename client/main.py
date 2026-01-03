from auth import Login, Logout
from token_storage import load_token
from api import get_my_profile

from app.utils.auth import decode_jwt_token


def main():

    # If no token, prompt user to login or sign up
    if not load_token():
        print("Welcome to ChatCLI 👋 \n")

        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")

        try:
            option = int(input("Select an option: "))
        except ValueError:
            print("Enter a valid option")


        match option:
            case 1:
                Login()


    else:
        # User is logged in
        username = decode_jwt_token(load_token().get("access_token"))

        print(f"Welcome back, {username} 👋 \n")

        print("1. View my profile")
        print("2. Send a message")
        print("3. View messages")
        print("4. View conversations")
        print("5. Logout")
            
        try:
            option = int(input("Select an option: "))
        except ValueError:
            print("Enter a valid option")
        
        match option:
            case 1:
                get_my_profile()
            case 5:
                Logout()