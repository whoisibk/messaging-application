from client.auth import Login



def main():
    print("Welcome to ChatCLI 👋\n")

    print("1. Login")
    print("2. Sign Up")
    print("3. Exit")

    try:
        option = int(input("Select an option: "))
    except ValueError:
        print("Enter a valid option")


    match option:
        case 1:
            userName= input("Username: ")
            password = input("Password: ")

            Login(userName, password)

