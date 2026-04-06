from typing import List  # import List type hint
from datetime import datetime

from app.database import session
from app.models import Conversation, Uuid, Message
from app.services.conversation_ops import update_last_message
from uuid import UUID

"""    Service functions for message operations    """


def create_message(
    senderId: Uuid,
    recipientId: Uuid,
    messageText: str,
    timestamp: datetime,
    conversationId: Uuid,
) -> Message:
    """Create a new message and add to the database"""
    new_message: Message = Message(
        senderId=senderId,
        recipientId=recipientId,
        messageText=messageText,
        timeStamp=timestamp,
        conversationId=conversationId,
    )
    db_session = session
    db_session.add(new_message)
    db_session.commit()

    update_last_message(conversationId, messageText)

    return new_message


def get_messagesInConversation_by_userId(
    userId: Uuid, conversationId: Uuid
) -> List[Message]:
    """get messages from a message sender with userId"""
    db_session = session
    messages = (
        db_session.query(Message)
        .filter(Message.senderId == userId, Message.conversationId == conversationId)
        .all()
    )
    return messages


def get_messages_by_conversation(conversationId: Uuid) -> List[Message]:
    """Retrieve messages by conversationId"""
    db_session = session
    messages: List[Message] = (
        db_session.query(Message)
        .filter(Message.conversationId == conversationId)
        .all()
    )
    db_session.commit()

    return messages


def get_message_by_Id(messageId: Uuid) -> Message:
    """Retrieve a message by messageId"""
    db_session = session
    message: Message = (
        db_session.query(Message).filter(Message.messageId == messageId).first()
    )
    db_session.commit()

    return message


def delete_message(messageId: Uuid) -> bool:
    """Delete a message by messageId"""
    db_session = session
    rows_deleted = (
        db_session.query(Message).filter(Message.messageId == messageId).delete()
    )
    db_session.commit()
    return True if rows_deleted > 0 else False


def get_undelivered_messages(userId: UUID) -> List[Message]:
    """Retrieve all undelivered messages for a user, ordered by timestamp."""
    db_session = session
    messages = (
        db_session.query(Message)
        .filter(Message.recipientId == userId, Message.delivered == False)
        .order_by(Message.timeStamp)
        .all()
    )
    return messages


def mark_messages_delivered(messageIds: List[UUID]) -> None:
    """Mark a list of messages as delivered."""
    if not messageIds:
        return
    db_session = session
    db_session.query(Message).filter(Message.messageId.in_(messageIds)).update(
        {"delivered": True}, synchronize_session="fetch"
    )
    db_session.commit()
