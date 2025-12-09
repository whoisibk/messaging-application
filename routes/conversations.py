from fastapi import APIRouter

router = APIRouter()

@router.get('/convo')
def convo():
    return {'This is a convo!'}