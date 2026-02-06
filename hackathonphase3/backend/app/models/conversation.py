"""
Conversation model for the AI Todo Chatbot application.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class ConversationBase(SQLModel):
    """Base model for Conversation containing shared attributes."""
    title: Optional[str] = Field(default=None, max_length=200)
    is_active: bool = Field(default=True)

class Conversation(ConversationBase, table=True):
    """
    Conversation model representing a chat session in the database.

    Attributes:
        id: Unique identifier for the conversation
        user_id: ID of the user who owns the conversation (no foreign key constraint)
        title: Optional title for the conversation (auto-generated if not provided)
        created_at: Timestamp when the conversation was created
        updated_at: Timestamp when the conversation was last updated
        is_active: Boolean indicating if the conversation is currently active
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int  # No foreign key constraint to avoid requiring user table
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ConversationCreate(ConversationBase):
    """Model for creating new conversations."""
    pass

class ConversationUpdate(SQLModel):
    """Model for updating existing conversations."""
    title: Optional[str] = Field(default=None, max_length=200)
    is_active: Optional[bool] = None