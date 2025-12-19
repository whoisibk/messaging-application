from fastapi import APIRouter, Depends, HTTPException, status

from typing import List
from services.conversation_ops import (
    conversations_for_user,
    Conversation,
    get_conversation_by_Id as get_convoId,
)
from users import get_current_user, User, Uuid

router = APIRouter()


@router.get("/conversations", response_model=List[Conversation])
def get_conversations(user: User = Depends(get_current_user)) -> List[Conversation]:
    """Retrieve all conversations a user has participated in"""

    conversations = conversations_for_user(user1_id=user.userId)
    if conversations is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No conversations were found",
        )
    return conversations


@router.get("conversations/{conversationId}", response_model=Conversation)
def get_conversation_by_Id(conversationId: Uuid) -> Conversation:
    """Retrieve conversation by ConversationId"""

    conversation = get_convoId(conversationId)
    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Conversation does not exist",
        )
    return conversation

# @router.delete()
# def delete_conversation()