from fastapi import APIRouter
from schemas import createUser, readUser, loginUser
from services.user_ops import *
from utils.auth import *

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
    return get_user_by_userName(new_user.userName)


@router.post("/login", response_model=str)
def login(user: loginUser) -> str:
    if get_user_by_userName(user.userName) is None:
        return "User not found"
    else:
        if verify_password(user.userName, hash_password(user.password)):
            pass
        
            userId = get_user_by_userName(user.userName).userId
            return create_jwt_token({"userId": str(userId)})
        else:
            return "Invalid Credentials"
    


@router.get("/me", response_model=readUser)
def current_user(token: str)->User:
    userId = decode_jwt_token(token)
    if userId:
        return get_user_by_Id(userId)
    return "Invalid or expired token"

@router.get("{users_id}", response_model=readUser)
def get_user_profile(userId: Uuid):
    return get_user_by_Id(userId)
