from pydantic import BaseModel, Field
from typing import Optional, List
from models import User, Message, Conversation, Uuid, DateTime as datetime


"""""" """''PYDANTIC MODELS FOR USER  """ """""" """"""


class createUser(BaseModel):
    """requirements for creating a user"""

    userName: str = Field(
        ..., min_length=3, max_length=15, description="username of User"
    )
    userEmail: str = Field(
        ..., min_length=12, max_length=256, description="user's email address"
    )
    password: str = Field(
        ..., min_length=5, max_length=256, description="plain password of user"
    )

    firstName: str = Field(
        ..., min_length=3, max_length=15, description="firstname of user"
    )
    lastName: str = Field(
        ..., min_length=3, max_length=15, description="lastname of user"
    )


class loginUser(BaseModel):
    """requirements for logging in"""

    userName: str = Field(..., description="user's username")
    password: str = Field(..., description="user's password")


class readUser(BaseModel):
    """requirements for reading a user"""

    userId: Uuid = Field(..., description="ID of user")
    userEmail: str = Field(
        ..., min_length=12, max_length=256, description="user's email address"
    )
    userName: str = Field(
        ..., min_length=3, max_length=15, description="username of User"
    )

    firstName: str = Field(
        ..., min_length=3, max_length=15, description="firstname of user"
    )
    lastName: str = Field(
        ..., min_length=3, max_length=15, description="lastname of user"
    )


"""""" """'' PYDANTIC MODELS FOR MESSAGES  """ """""" """"""


class createMessage(BaseModel):
    senderId: Uuid = Field(..., description="ID of sender")
    recipientId: Uuid = Field(..., description="ID of recipient")

    messageText: str = Field(
        ..., min_length=1, max_length=256, description="the message itself"
    )


class sentMessage(BaseModel):
    status_code: int = Field(..., description="HTTP Status Code of Message")
    senderId: Uuid = Field(..., description="ID of sender")
    messageText: str = Field(
        ..., min_length=1, max_length=256, description="the message itself"
    )
    timestamp: datetime = Field(..., description="timestamp of message")


class readMessage(BaseModel):
    messageId: Uuid = Field(..., description="ID of message")
    senderId: Uuid = Field(..., description="ID of sender")
    recipientId: Uuid = Field(..., description="ID of recipient")
    conversationId: Uuid = Field(..., description="ID of conversation")

    messageText: str = Field(
        ..., min_length=1, max_length=256, description="the message itself"
    )
    timestamp: datetime = Field(..., description="timestamp of message")


"""""" """''PYDANTIC MODELS FOR CONVERSATION  """ """""" """"""


class Conversation(BaseModel):
    conversationId: Uuid = Field(..., description="ID of conversation")
    user1_Id: Uuid = Field(..., description="ID of first user")
    user2_Id: Uuid = Field(..., description="ID of second user")
    dateCreated: datetime = Field(..., description="date conversation initiated")
    lastMessage: str = Field(
        ..., min_length=1, max_length=256, description="last message in conversation"
    )
