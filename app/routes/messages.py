from fastapi import APIRouter

router = APIRouter()

@router.get('/test')
def message():
    return {'This is a message!'}
