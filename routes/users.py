from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def user():
    return {'Hi, I am a user!'}
