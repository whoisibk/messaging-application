from sys import exit
import asyncio

from client.auth import SignUp, Login, Logout
from client.token_storage import load_token
from client.actions import view_profile, start_chat, view_messages, view_conversations

from app.utils.auth import decode_jwt_token


def main():
    while True:
        load_token_ = load_token()
        if not load_token_ or (username := decode_jwt_token(dict(load_token_).get("access_token"))) is None:
            username = user_not_logged_in()
        user_logged_in(username)


def user_not_logged_in():
    """Prompt login/signup until successful. Returns username."""
    print("\n\n\t\t----------------- Welcome to ChatCLI 👋 -----------------\n")

    while True:
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")

        try:
            option = int(input("\nSelect an option: "))
            print()
        except ValueError:
            print("Enter a valid option\n")
            continue

        match option:
            case 1:
                username = Login()
                print(f"\n\t\t\t\tLogged in as {username}")
                return username
            case 2:
                print(SignUp())
                username = Login()
                print(f"\n\t\t\t\tLogged in as {username}")
                return username
            case 3:
                exit("The application has been closed.")
            case _:
                print("Enter a valid option\n")


def user_logged_in(username):
    """Main menu loop for a logged-in user."""
    while True:
        print(f"\nWelcome back, {username} 👋 \n")
        print("1. View my profile")
        print("2. Send a message")
        print("3. View messages")
        print("4. View conversations")
        print("5. Logout")

        try:
            option = int(input("\nSelect an option: "))
            print()
        except ValueError:
            print("Enter a valid option")
            continue

        match option:
            case 1:
                view_profile()
            case 2:
                start_chat()
            case 3:
                view_messages()
            case 4:
                view_conversations()
            case 5:
                Logout()
                return
            case _:
                print("Enter a valid option")


if __name__ == "__main__":
    main()
