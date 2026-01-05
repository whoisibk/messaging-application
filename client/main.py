from sys import exit

from client.auth import SignUp, Login, Logout
from client.token_storage import load_token
from client.api import get_my_profile

from app.utils.auth import decode_jwt_token

def main():
    if not load_token():
        # If no token, prompt user to login or sign up 
        user_not_logged_in()

        # After login/signup, run user_logged_in function
        user_logged_in()
    else:
        # User is already logged in
        user_logged_in()
        

def user_not_logged_in():
    """Function to handle a user who is not logged in"""

    print("\n\n\t\t----------------- Welcome to ChatCLI 👋 -----------------\n")

    print("1. Login")
    print("2. Sign Up")
    print("3. Exit")

    try:
        option = int(input("\nSelect an option: "))
        print()
    except ValueError:
        print("Enter a valid option")

    match option:
        case 1:
            # if the user is logged out 
            print(Login())

        case 2:
            # new user sign up 
            print(SignUp())
            print(Login())

        case 3:
            exit("The application has been closed.")

def user_logged_in():
    """Function to handle user who is logged in"""

    username = decode_jwt_token(dict(load_token()).get("access_token"))

    print(f"Welcome back, {username} 👋 \n")

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

    match option:
        case 1:
            print(get_my_profile())
        case 5:
            Logout()



if __name__ == "__main__":
    main()  
