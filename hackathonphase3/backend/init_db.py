"""
Script to initialize the database with required tables.
"""

from sqlmodel import SQLModel
from app.database.session import engine
from app.models.task import Task
from app.models.conversation import Conversation
from app.models.message import Message

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()