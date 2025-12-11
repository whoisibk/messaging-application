from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# base class for ORM
Base = declarative_base()  

# defining models for db tables
class User(Base):
    __tablename__ = 'user'

    userId = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    userName = Column(String(15), unique=True, nullable=False)
    userEmail = Column(String(100), unique=True, nullable=False)
    passwordHash = Column(String(255), nullable=False)
    dateCreated = Column(DateTime, nullable=False)


    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)


class Message(Base):
    __tablename__ = 'message'

    messageId = Column(Integer, autoincrement=True, nullable=False, primary_key=True) 

    # retrieve sender and recipient via userId, 
    senderId = Column(Integer, ForeignKey('user.userId', ondelete='CASCADE'), nullable=False) 
    recipientId = Column(Integer, ForeignKey('user.userId', ondelete='CASCADE'), nullable=False, unique=True)

    # retrieve conversation (of which message is a part of) via conversationId
    conversationId = Column(Integer, ForeignKey('conversation.conversationId', ondelete='CASCADE'), nullable=False)
    
    messageText  = Column(String(250), nullable=False)
    timeStamp = Column(DateTime, nullable=False)
    
class Conversation(Base):
    __tablename__ = 'conversation'

    conversationId = Column(Integer, nullable=False, unique=True, primary_key=True)

    # retrieve conversation participants via userId
    user1_Id = Column(Integer, ForeignKey('user.userId'), nullable=False, unique=True)
    user2_Id = Column(Integer, ForeignKey('user.userId'), nullable=False, unique=True)
