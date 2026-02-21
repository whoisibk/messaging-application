from app.models import User
from uuid import UUID as Uuid
from app.database import session
from datetime import datetime

from app.utils.auth import verify_password


"""    Service functions for user operations    """


def create_user(
    userName, userEmail, passwordHash: str, firstName, lastName, dateCreated: datetime
) -> User:
    """# Create a new user and add to the database"""
    new_user: User = User(
        userName=userName,
        userEmail=userEmail,
        # password will be hashed in the route handler before assigning
        passwordHash=passwordHash,
        firstName=firstName,
        lastName=lastName,
        dateCreated=dateCreated,
    )

    db_session = session
    db_session.add(new_user)
    db_session.commit()

    return new_user

def get_user_by_Id(userId: Uuid) -> User:
    """Retrieve a user from the database by userId"""
    db_session = session
    user: User = db_session.query(User).filter(User.userId == userId).first()
    return user if user else None

def get_user_by_userName(username) -> User:
    """Retrieve a user from the database by userName"""

    db_session = session
    user: User = db_session.query(User).filter(User.userName == username).first()
    return user if user else None

def get_user_by_email(userEmail) -> User:
    """Retrieve a user from the database by email"""
    db_session = session
    user: User = db_session.query(User).filter(User.userEmail == userEmail).first()
    return user if user else None


def get_userId_by_userName(userName) -> Uuid:
    """Retrieve userId using userName"""
    db_session = session

    user: User = db_session.query(User).filter(User.userName == userName).first()
    return user.userId if user else None


def verify_user_credentials(username, password: str) -> bool:
    """# Verify user credentials"""
    
    user: User = get_user_by_userName(username)
    if user and verify_password(password, user.passwordHash):
        return True
    return False


# def update_user(userName: str) -> User:
#     db_session = session
#     user: User = db_session.query(User).filter(User.userName==userName).first()
