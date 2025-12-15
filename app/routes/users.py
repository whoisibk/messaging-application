from fastapi import APIRouter
from schemas import createUser, readUser
from services.user_ops import *
from utils.hashing import *

router = APIRouter()


@router.post("/signup", response_model=readUser)
def signup(user: createUser) -> User:
    new_user: readUser = create_user(
        firstName=user.firstName,
        lastName=user.lastName,
        userName=user.userName,
        userEmail=user.userEmail,
        passwordHash=hash_password(user.password),
        dateCreated=datetime.now(),
    )
    # return newly added user
    return get_user_by_userName(user.userName)


@router.post("/login", response_model=readUser)
def login(userName, password) -> User:
    if verify_password(userName, hash_password(password)):
        return get_user_by_userName(userName)
    else:
        return "Invalid Credentials"
    
@router.get("me", response_model=readUser)
def current_user(userName):
    return get_user_by_userName(userName)


@router.get('{users_id}', response_model=readUser)
def get_user_profile(userId: Uuid):
    return get_user_by_Id(userId)
