from models import Conversation, Uuid
from database import session


def create_conversation(user1_Id: Uuid, user2_id: Uuid)-> Conversation:
    db_session = session

    new_conversation = Conversation(
        user1_Id = user1_Id,
        user2_id = user2_id
    )

    db_session.add(new_conversation)
    db_session.commit()

    return new_conversation

def get_conversation_by_Id(conversationId: Uuid) -> Conversation:
    db_session = session
    conversation = db_session.query(Conversation).filter(Conversation.conversationId==conversationId).first()

    return conversation
