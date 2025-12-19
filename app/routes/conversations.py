from fastapi import APIRouter, Depends, HTTPException, status

from typing import List
from services.conversation_ops import conversations_for_user, Conversation
from users import get_current_user, User

router = APIRouter()


@router.get("/test")
def get_conversation(user: User = Depends(get_current_user)) -> List[Conversation]:
    """Retrieve all conversations a user has participated in"""

    conversations = conversations_for_user(user1_id=user.userId)
    if conversations is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No conversations were found",
        )
    return conversations
