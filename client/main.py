from sys import exit
import asyncio

from client.auth import SignUp, Login, Logout
from client.token_storage import load_token
from client.api import get_my_profile, get_websocket_url, get_messages, conversations, get_user_by_id
from client.ws import chat_session

from app.utils.auth import decode_jwt_token

def main():
    # returns None if token expires, else returns the username

    # username = decode_jwt_token(dict(load_token()).get("access_token"))
    load_token_  = load_token()

    if not load_token_ or (username := decode_jwt_token(dict(load_token_).get("access_token"))) is None:
        # If no token or , prompt user to login or sign up 
        user_not_logged_in()

        # After login/signup, run user_logged_in function
        user_logged_in(username_)
    else:
        # User is already logged in
        user_logged_in(username)
        

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
            global username_
            username_ = Login()
            print(f"\n\t\t\t\tLogged in as {username_}")

        case 2:
            # new user sign up 
            print(SignUp())

            username_ = Login()
            print(f"\n\t\t\t\tLogged in as {username_}")
            
        case 3:
            exit("The application has been closed.")

        case _:
            print("Enter a valid option")

def user_logged_in(username):
    """Function to handle user who is logged in"""


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

    match option:
        case 1:
            # get my profile
            get_my_profile()
        case 2:
            # open realtime chat session
            ws_url = get_websocket_url()
            asyncio.run(chat_session(ws_url))
        case 3:
            # view messages in a conversation
            me = get_my_profile()
            my_id = str(me["userId"])
            convos = conversations()
            if not convos:
                print("You have no conversations.")
            else:
                other_users = {}
                for i, c in enumerate(convos, 1):
                    other_id = c["user2_Id"] if str(c["user1_Id"]) == my_id else c["user1_Id"]
                    other = get_user_by_id(other_id)
                    other_users[i] = (c, other["userName"])
                    last = c.get("lastMessage") or "no messages yet"
                    print(f"{i}. {other['userName']} — {last}")

                try:
                    pick = int(input("\nSelect a conversation: "))
                    convo, other_name = other_users[pick]
                except (ValueError, KeyError):
                    print("Invalid selection.")
                    return

                messages = get_messages(convo["conversationId"])
                print()
                for msg in messages:
                    sender = "You" if str(msg["senderId"]) == my_id else other_name
                    ts = msg["timestamp"][:16].replace("T", " ")
                    print(f"[{ts}] {sender}: {msg['messageText']}")
        case 4:
            # view all conversations
            me = get_my_profile()
            my_id = str(me["userId"])
            convos = conversations()
            if not convos:
                print("You have no conversations.")
            else:
                for i, c in enumerate(convos, 1):
                    other_id = c["user2_Id"] if str(c["user1_Id"]) == my_id else c["user1_Id"]
                    other = get_user_by_id(other_id)
                    last = c.get("lastMessage") or "no messages yet"
                    print(f"{i}. {other['userName']} — {last}")
        case 5:
            Logout()


if __name__ == "__main__":
    main()  
