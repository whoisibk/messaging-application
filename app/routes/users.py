from fastapi import APIRouter, HTTPException, Depends, status, WebSocket

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from app.schemas import createUser, readUser
from app.services.user_ops import *
from app.utils.auth import *

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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.post("/login", response_model=dict)
def login(user_login: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint for user login.

    This endpoint uses the OAuth2 standard password flow. It expects the
    credentials to be sent as form data (URL-encoded) rather than JSON.

    Args:
        user_login (OAuth2PasswordRequestForm): An object containing the
            'username' and 'password' extracted from the request form.

    Returns:
        dict: A dictionary containing the 'access_token' and 'token_type'.

    Raises:
        HTTPException: 401 error if authentication fails.
    """
    username, password = user_login.username, user_login.password
   
    if not verify_user_credentials(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

    access_token = create_jwt_token(data={"username": username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    Retrieve the current authenticated user's details.

    This function extracts the JWT token from the HTTP Authorization header,
    decodes it to obtain the username, and returns the corresponding user object.

    Args:
        token (str): The JWT token from the Authorization header,
            injected via the oauth2_scheme dependency.

    Returns:
        User: The user object containing details of the currently authenticated user.

    Raises:
        HTTPException: With status code 401 UNAUTHORIZED if the token is invalid,
            expired, or does not contain a valid userName claim.
    """
    userName = decode_jwt_token(token)
    if not userName:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired Token",
        )
    return get_user_by_userName(userName)


def get_current_user_ws(websocket: WebSocket) -> User:
    """
    Retrieve current user for WebSocket connections using the Authorization header.

    Expects header: Authorization: Bearer <token>
    """
    token = websocket.query_params.get("token")

    # Fallback for clients that send JWT in Authorization header.
    if token is None:
        auth_header = websocket.headers.get("Authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            token = auth_header.split(" ", 1)[1]

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
        )

    userName = decode_jwt_token(token)
    if not userName:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired Token",
        )

    user = get_user_by_userName(userName)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


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


@router.get("/profile/{userId}", response_model=readUser)
def get_user_profile(userId: Uuid) -> User:
    """
    Endpoint to get a user's profile by userId
    Args:
        userId (Uuid): ID of the user
    Returns:
        User: Details of the user
    """
    return get_user_by_Id(userId)


@router.get("/lookup/{userName}", response_model=readUser)
def get_user_by_username_lookup(
    userName: str,
    current_user: User = Depends(get_current_user),
) -> User:
    """Retrieve user profile by username for recipient resolution."""
    user = get_user_by_userName(userName)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
