"""
Message model for the AI Todo Chatbot application.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from sqlalchemy import JSON

class MessageRole(str, Enum):
    """Enumeration of possible message roles."""
    user = "user"
    assistant = "assistant"
    system = "system"

class MessageBase(SQLModel):
    """Base model for Message containing shared attributes."""
    role: MessageRole
    content: str = Field(min_length=1)
    tool_calls: Optional[dict] = Field(default=None, sa_type=JSON)
    tool_responses: Optional[dict] = Field(default=None, sa_type=JSON)

class Message(MessageBase, table=True):
    """
    Message model representing a message in a conversation.

    Attributes:
        id: Unique identifier for the message
        conversation_id: Foreign key linking to the conversation
        role: Role of the message sender (user/assistant/system)
        content: Text content of the message
        timestamp: When the message was sent
        tool_calls: JSON field storing tool call information
        tool_responses: JSON field storing tool response information
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MessageCreate(MessageBase):
    """Model for creating new messages."""
    pass

class MessageUpdate(SQLModel):
    """Model for updating existing messages."""
    content: Optional[str] = Field(default=None, min_length=1)
    tool_calls: Optional[dict] = Field(default=None, sa_type=JSON)
    tool_responses: Optional[dict] = Field(default=None, sa_type=JSON)