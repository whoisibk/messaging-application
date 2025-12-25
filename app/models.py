import uuid

from sqlalchemy.dialects.postgresql import UUID as Uuid  # id generator
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey  # column datatypes
from sqlalchemy.ext.declarative import declarative_base

# base class for ORM
Base = declarative_base()


# defining models for db tables
class User(Base):
    __tablename__ = "user"

    userId = Column(
        Uuid(as_uuid=True), unique=True, primary_key=True, default=uuid.uuid4
    )
    userName = Column(String(15), unique=True, nullable=False)
    userEmail = Column(String(100), unique=True, nullable=False)
    passwordHash = Column(String(255), nullable=False)
    dateCreated = Column(DateTime, nullable=False)

    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)


class Message(Base):
    __tablename__ = "message"

    messageId = Column(
        Uuid(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4
    )

    # retrieve sender and recipient via userId,
    senderId = Column(
        Uuid(as_uuid=True),
        ForeignKey("user.userId", ondelete="CASCADE"),
        nullable=False,
    )
    recipientId = Column(
        Uuid(as_uuid=True),
        ForeignKey("user.userId", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # retrieve conversation (of which message is a part of) via conversationId
    conversationId = Column(
        Uuid(as_uuid=True),
        ForeignKey("conversation.conversationId", ondelete="CASCADE"),
        nullable=False,
    )

    messageText = Column(String(250), nullable=False)
    timeStamp = Column(DateTime, nullable=False)


class Conversation(Base):
    __tablename__ = "conversation"

    conversationId = Column(
        Uuid(as_uuid=True),
        nullable=False,
        unique=True,
        primary_key=True,
        default=uuid.uuid4,
    )

    # retrieve conversation participants via userId
    user1_Id = Column(
        Uuid(as_uuid=True), ForeignKey("user.userId"), nullable=False, unique=True
    )
    user2_Id = Column(
        Uuid(as_uuid=True), ForeignKey("user.userId"), nullable=False, unique=True
    )
