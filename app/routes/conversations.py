from fastapi import APIRouter

router = APIRouter()

@router.get('/test')
def conversation():
    return {'This is a convo!'}