from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from uuid import UUID as Uuid

from app.schemas import readMessage
from app.services.message_ops import *
from app.services.conversation_ops import *
from app.routes.users import get_current_user, User
from app.services.user_ops import get_user_by_Id

router = APIRouter()


# @router.post("/save_message", response_model=sentMessage)
def save_message(recipientId: Uuid, messageText: str, senderId: Uuid) -> dict:
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

    recipient = get_user_by_Id(recipientId)
    if recipient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipient not found",
        )

    existing_conversation_id = get_conversationId_between_users(
        user1_Id=senderId,
        user2_Id=recipientId,
    )
    if existing_conversation_id is None:
        conversationId = create_conversation(
            user1_Id=senderId,
            user2_Id=recipientId,
        ).conversationId
    else:
        conversationId = existing_conversation_id

    """ saves message to the database so it can be fetched later """
    message_info = create_message(
        senderId=senderId,
        recipientId=recipientId,
        messageText=messageText,
        timestamp=datetime.now(),
        conversationId=conversationId,
    )

    return {
        "messageId": str(message_info.messageId),
        "conversationId": message_info.conversationId,
        "timestamp": message_info.timeStamp,
        "message": message_info.messageText,
        "senderId": message_info.senderId,
        "recipientId": message_info.recipientId,
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
    return [
        {
            "messageId": message.messageId,
            "senderId": message.senderId,
            "recipientId": message.recipientId,
            "conversationId": message.conversationId,
            "messageText": message.messageText,
            "timestamp": message.timeStamp,
        }
        for message in messages
    ]
