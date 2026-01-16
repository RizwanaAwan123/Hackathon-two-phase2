from sqlmodel import Session, select
from ..models.user import User, UserCreate
from typing import Optional

def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user in the database"""
    db_user = User(
        email=user_create.email,
        username=user_create.username,
        hashed_password=user_create.password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get a user by email"""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user

def get_user_by_id(session: Session, user_id: str) -> Optional[User]:
    """Get a user by ID"""
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user