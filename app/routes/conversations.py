from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import Conversation as Conversation_

from typing import List
from app.services.conversation_ops import (
    conversations_for_user,
    Conversation,
    get_conversation_by_Id as get_convoId,
    delete_conversation,
)
from app.routes.users import get_current_user, User, Uuid

router = APIRouter()


@router.get("/get-conversations", response_model=List[Conversation_])
def get_conversations(user: User = Depends(get_current_user)) -> List[Conversation_]:
    """Retrieve all conversations a user has participated in"""

    conversations = conversations_for_user(user1_id=user.userId)
    if conversations is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No conversations were found",
        )
    return conversations


@router.get("/{conversationId}", response_model=Conversation_)
def get_conversation_by_Id(conversationId: Uuid) -> Conversation_:
    """Retrieve conversation by ConversationId"""

    conversation = get_convoId(conversationId)
    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Conversation does not exist",
        )
    return conversation


@router.delete('/{conversationId}')
def delete__conversation(conversationId: Uuid):
    """Delete a conversation and all associated messages"""
    success = delete_conversation(conversationId)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return {"detail": "Conversation deleted successfully"}