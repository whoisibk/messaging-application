from app.models import Conversation, Uuid
from app.database import session
from typing import List
from sqlalchemy import and_, or_


def _normalize_participants(user1_Id: Uuid, user2_Id: Uuid) -> tuple[Uuid, Uuid]:
    # Keep one consistent ordering so A<->B maps to a single conversation row.
    return (user1_Id, user2_Id) if str(user1_Id) < str(user2_Id) else (user2_Id, user1_Id)


def create_conversation(user1_Id: Uuid, user2_Id: Uuid) -> Conversation:
    db_session = session

    user1_Id, user2_Id = _normalize_participants(user1_Id, user2_Id)

    new_conversation = Conversation(user1_Id=user1_Id, user2_Id=user2_Id)

    db_session.add(new_conversation)
    db_session.commit()

    return new_conversation


def get_conversation_by_Id(conversationId: Uuid) -> Conversation:
    db_session = session
    conversation = (
        db_session.query(Conversation)
        .filter(Conversation.conversationId == conversationId)
        .first()
    )

    db_session.commit()

    return conversation


def get_conversationId_between_users(user1_Id: Uuid, user2_Id: Uuid) -> Uuid | None:
    db_session = session
    conversation = (
        db_session.query(Conversation)
        .filter(
            or_(
                and_(
                    Conversation.user1_Id == user1_Id,
                    Conversation.user2_Id == user2_Id,
                ),
                and_(
                    Conversation.user1_Id == user2_Id,
                    Conversation.user2_Id == user1_Id,
                ),
            )
        )
        .first()
    )
    db_session.commit()

    return conversation.conversationId if conversation else None


def conversations_for_user(user1_id: Uuid) -> List[Conversation]:
    db_session = session
    conversations = (
        db_session.query(Conversation).filter(Conversation.user1_Id == user1_id).all()
    )

    db_session.commit()

    return conversations


def delete_conversation(conversationId: Uuid) -> bool:
    db_session = session
    rows_deleted = (
        db_session.query(Conversation)
        .filter(Conversation.conversationId == conversationId)
        .first()
    )
    db_session.commit()

    return True if rows_deleted > 0 else False
