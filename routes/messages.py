from fastapi import APIRouter

router = APIRouter()

@router.get('/messages')
def message():
    return {'This is a message!'}
