from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
)

from schemas import createUser, readUser, loginUser
from services.user_ops import *
from utils.auth import *

router = APIRouter()


@router.post("/signup", response_model=readUser)
def signup(user: createUser) -> User:
    """
    Endpoint for user signup
    Args:
        user (createUser): User signup details
    Returns:
        User: Newly created user details
    """

    new_user: readUser = create_user(
        firstName=user.firstName,
        lastName=user.lastName,
        userName=user.userName,
        userEmail=user.userEmail,
        passwordHash=hash_password(user.password),
        dateCreated=datetime.now(),
    )
    # return newly added user
    return get_user_by_userName(new_user.userName)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/login", response_model=dict)
def login(userLogin: OAuth2PasswordRequestForm = Depends()) -> dict:
    """
    Endpoint for user login.

    This endpoint uses the OAuth2 standard password flow. It expects the
    credentials to be sent as form data (URL-encoded) rather than JSON.

    Args:
        form_data (OAuth2PasswordRequestForm): An object containing the
            'username' and 'password' extracted from the request form.

    Returns:
        dict: A dictionary containing the 'access_token' and 'token_type'.

    Raises:
        HTTPException: 401 error if authentication fails.
    """
    userName, passwordhash = userLogin.username, hash_password(userLogin.password)

    if not verify_password(userName, passwordhash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_jwt_token(data={"userName": userName})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
) -> User:
    """
    Retrieve the current authenticated user's details.

    This function extracts the JWT token from the HTTP Authorization header,
    decodes it to obtain the username, and returns the corresponding user object.

    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP Authorization credentials
            containing the JWT token, injected via the oauth2_scheme dependency.

    Returns:
        User: The user object containing details of the currently authenticated user.

    Raises:
        HTTPException: With status code 401 UNAUTHORIZED if the token is invalid,
            expired, or does not contain a valid userName claim.
    """
    token = credentials.credentials
    userName = decode_jwt_token(token).get("userName")
    if not userName:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired Token",
        )
    return get_user_by_userName(userName)


@router.get("/profile/me", response_model=readUser)
def get_my_profile(current_user: User = Depends(get_current_user)) -> User:
    """
    Endpoint to get the profile of the currently authenticated user
    Args:
        current_user (User): The currently authenticated user, injected via dependency
    Returns:
        User: Details of the current user
    """
    return current_user


@router.get("profile/{user_id}", response_model=readUser)
def get_user_profile(userId: Uuid) -> User:
    """
    Endpoint to get a user's profile by userId
    Args:
        userId (Uuid): ID of the user
    Returns:
        User: Details of the user
    """
    return get_user_by_Id(userId)
