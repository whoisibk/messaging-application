from fastapi import APIRouter

router = APIRouter()

@router.get('/test')
def signup():
    return {'Hi, I am a user!'}
