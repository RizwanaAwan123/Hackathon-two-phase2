from sqlmodel import create_engine, Session
from typing import Generator
from ..config.settings import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session