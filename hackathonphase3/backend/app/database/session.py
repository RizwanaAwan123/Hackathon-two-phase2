"""
Database session management for the AI Todo Chatbot application.
"""

from sqlmodel import create_engine, Session
from app.core.config import settings

# Create the database engine
# For SQLite, we need to handle the URL differently
if settings.DATABASE_URL.startswith("sqlite"):
    # For SQLite, disable pooling which can cause issues
    engine = create_engine(settings.DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session():
    """
    Generator that yields a database session.

    This is used as a dependency in FastAPI routes to provide
    database sessions to route handlers.
    """
    with Session(engine) as session:
        yield session