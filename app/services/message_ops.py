from models import Message
from datetime import datetime
from database import session
from models import Conversation, Uuid

def create_message(senderId: int, recipientId:int, messageText:str, timestamp: datetime) -> str:
    new_message: Message = Message(senderId=senderId,
                          recipientId=recipientId,
                          messageText=messageText,
                          timestamp=timestamp,
                          )
    db_session = session
    db_session.add(new_message)
    db_session.commit()

    return new_message

def get_messages_by_conversation(conversationId: int):

    db_session = session
    db_session.query(Conversation).filter(conversationId=conversationId)



