from typing import Tuple
from models import User
from database import session

# from utils.hashing import hash_password, verify_password


def create_user(
    userName, userEmail, passwordHash, firstName, lastName, dateCreated
) -> User:

    # Create a new user and add to the database
    new_user: User = User(
        userName=userName,
        userEmail=userEmail,
        # password will be hashed in the route handler before calling this function
        passwordHash=passwordHash,
        firstName=firstName,
        lastName=lastName,
        dateCreated=dateCreated,
    )

    db_session = session
    db_session.add(new_user)
    db_session.commit()

    return new_user


def get_user_by_userName(userName: str) -> User:
    # Retrieve a user from the database by userName
    db_session = session
    user: User = db_session.query(User).filter(User.userName == userName).first()
    return user


def get_user_by_userId(userId: int) -> User:
    # Retrieve a user from the database by userId
    db_session = session
    user: User = db_session.query(User).filter(User.userId == userId).first()
    return user


def verify_user_credentials(userName:str, passwordHash:str) -> bool:
    # Verify user credentials
    user: User = get_user_by_userName(userName)
    if user.passwordHash == passwordHash:
        return True
    return False

# def update_user(userName: str) -> User:
#     db_session = session
#     user: User = db_session.query(User).filter(User.userName==userName).first()


