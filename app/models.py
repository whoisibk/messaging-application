from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# base class for ORM
Base = declarative_base()  

# defining models for db tables
class User(Base):
    userId = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    userName = Column(String(15), unique=True, nullable=False)
    userEmail = Column(String(100), unique=True, nullable=False)
    passwordHash = Column(String(255), nullable=False)
    dateCreated = Column(DateTime, nullable=False)
    # rel_to_msgs = Column(Integer, ForeignKey('messageId', ondelete='CASCADE'), nullable=False)


    firstName = Column(String(50), nullable=False)
    lastName = Column(String(50), nullable=False)


class Message(Base):
    messageId = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    senderId = Column(Integer, nullable=False, unique=True)
    recipientId = Column(Integer, nullable=False, unique=True)
    rel_to_conversation = Column(Integer, ForeignKey('conversationId', ondelete='CASCADE'), nullable=False)
    
    messageTxt  = Column(String(250), nullable=False)
    timeStamp = Column(DateTime, nullable=False)
    
class Conversation(Base):
    conversationId = Column(Integer, nullable=False, unique=True, primary_key=True)
    user1_Id = Column(Integer, nullable=False, unique=True)
    user2_Id = Column(Integer, nullable=False, unique=True)