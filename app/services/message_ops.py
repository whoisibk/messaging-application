from typing import List  # import List type hint
from models import Conversation, Uuid, Message
from datetime import datetime
from database import session


"""    Service functions for message operations    """


def create_message(
    senderId: Uuid, recipientId: Uuid, messageText, timestamp: datetime
) -> Message:
    """Create a new message and add to the database"""
    new_message: Message = Message(
        senderId=senderId,
        recipientId=recipientId,
        messageText=messageText,
        timestamp=timestamp,
    )
    db_session = session
    db_session.add(new_message)
    db_session.commit()

    return new_message


def get_messages_by_conversation(conversationId: Uuid) -> List[Message]:
    """Retrieve messages by conversationId"""
    db_session = session
    messages: List[Message] = (
        db_session.query(Conversation)
        .filter(Conversation.conversationId == conversationId)
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
