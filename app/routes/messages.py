from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import List

from app.services.message_ops import create_message
from app.schemas import sentMessage, createMessage, readMessage
from app.services.message_ops import *
from app.services.conversation_ops import *
from app.utils.auth import create_jwt_token
from app.routes.users import get_current_user, User, Uuid

router = APIRouter()


# @router.post("/save_message", response_model=sentMessage)
def save_message(recipientId: Uuid, messageText: str, senderId: Uuid) -> sentMessage:
    """
    Stores message in database before forwarding to recipient
    Args:
        recipientId (Uuid): ID of the message's recipient
        messageText(str)): message text content
        senderId (Uuid): ID of the message's sender

    # Return:
    #     (sentMessage)
    #         status_code: int
    #         senderId: Uuid
    #         messageText: str
    #         timestamp: datetime
    #         conversationId: Uuid
    """

    """extracts convoId if not none, else create and then extract"""
    get_conv = get_conversationId_between_users(user1_Id=senderId, user2_Id=recipientId)
    if get_conv is None:
        conversationId = create_conversation(
            user1_Id=senderId, user2_id=recipientId
        ).conversationId
    else:
        conversationId = get_conv.conversationId

    """ saves message to the database so it can be fetched later """
    message_info = create_message(
        senderId=senderId,
        recipientId=recipientId,
        messageText=messageText,
        timestamp=datetime.now(),
        conversationId=conversationId,
    )

    return {
        "status": 200,
        "conversationId": message_info.conversationId,
        "timestamp": message_info.timestamp,
        "message": message_info.messageText,
        "sent by": message_info.senderId,
    }

    # realtime convo will be integrated later during websockets


# @router.get("/{}/conversations")


@router.get("/{conversationId}", response_model=List[readMessage])
def get_messages(
    conversationId: Uuid, user: User = Depends(get_current_user)
) -> List[readMessage]:
    """Retrieve messages sent by user within a conversation"""

    messages: List[readMessage] = get_messagesInConversation_by_userId(
        userId=user.userId, conversationId=conversationId
    )
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Conversation not found",
        )
    return messages
