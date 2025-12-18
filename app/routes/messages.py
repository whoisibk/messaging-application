from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer

from services.message_ops import create_message
from schemas import sentMessage, createMessage
from services.message_ops import *
from services.conversation_ops import *
from utils.auth import create_jwt_token
from users import get_current_user, User, Uuid

router = APIRouter()


@router.post("/send_message", response_model=sentMessage)
def send_message(
    recipientId: Uuid, messageText: str, sender: User = Depends(get_current_user)
) -> sentMessage:
    """
    Endpoint for sending a message from one user to another
    Args:
        recipientId (Uuid): ID of the message's recipient
        messageText(str)): message text content
        sender (User): User model of the message's sender
    """

    """extracts convoId if not none, else create and then extract"""
    get_conv = get_conversation_between_users()
    if get_conv is None:
        conversationId = create_conversation(
            user1_Id=sender.userId, user2_id=recipientId
        ).conversationId
    else:
        conversationId = get_conv.conversationId

    """ saves message to the database so it can be fetched later """
    message_info = create_message(
        recipientId=recipientId,
        messageText=messageText,
        senderId=sender.userId,
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

@router.get("/messages", response_model=List[Message])
def get_messages(conversationId: Uuid) ->List[Message]:
    messages = get_messages_by_conversation(conversationId)
    if not messages:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Conversation not found",
            )
    return messages
