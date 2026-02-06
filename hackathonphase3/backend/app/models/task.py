"""
Task model for the AI Todo Chatbot application.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class TaskStatus(str, Enum):
    """Enumeration of possible task statuses."""
    pending = "pending"
    completed = "completed"

class TaskBase(SQLModel):
    """Base model for Task containing shared attributes."""
    content: str = Field(min_length=1, max_length=500)
    status: TaskStatus = Field(default=TaskStatus.pending)

class Task(TaskBase, table=True):
    """
    Task model representing a todo item in the database.

    Attributes:
        id: Unique identifier for the task
        content: The text content of the task
        status: Current status of the task (pending/completed)
        created_at: Timestamp when the task was created
        updated_at: Timestamp when the task was last updated
        user_id: ID of the user who owns the task (no foreign key constraint)
        conversation_id: Foreign key linking to the conversation where task was created
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int  # No foreign key constraint to avoid requiring user table
    conversation_id: int = Field(foreign_key="conversation.id")

class TaskCreate(TaskBase):
    """Model for creating new tasks."""
    pass

class TaskUpdate(SQLModel):
    """Model for updating existing tasks."""
    content: Optional[str] = Field(default=None, min_length=1, max_length=500)
    status: Optional[TaskStatus] = None