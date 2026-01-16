from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from typing import Annotated, Dict, Any
from ..database.database import get_session
from ..models.user import User, UserCreate, UserRead
from ..services.auth_service import create_access_token, verify_password, hash_password
from ..services.user_service import create_user, get_user_by_email

router = APIRouter()

@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(user_create: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = hash_password(user_create.password)
    user_create.password = hashed_password

    # Create the user
    db_user = create_user(session, user_create)
    return db_user

@router.post("/signin")
async def signin(request: Request, session: Session = Depends(get_session)):
    try:
        user_data = await request.json()
        email = user_data.get("email")
        password = user_data.get("password")

        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email and password required"
            )

        user = get_user_by_email(session, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        access_token = create_access_token(data={"sub": user.email})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request format"
        )

@router.post("/signout")
def signout():
    # In a real implementation, you might want to invalidate the token
    # For now, we just return a success message
    return {"message": "Successfully signed out"}