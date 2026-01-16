from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from ..database.database import get_session
from ..middleware.auth import get_current_user
from ..models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from ..models.user import User
from ..services.todo_service import (
    create_todo_for_user,
    get_todos_by_user,
    get_todo_by_id_and_user,
    update_todo,
    delete_todo,
    toggle_todo_completion
)

router = APIRouter()

@router.get("/", response_model=List[TodoRead])
def read_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all todos for the current user"""
    todos = get_todos_by_user(session, current_user.id)
    return todos

@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new todo for the current user"""
    return create_todo_for_user(session, todo, current_user.id)

@router.put("/{todo_id}", response_model=TodoRead)
def update_todo_item(
    todo_id: str,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update an existing todo"""
    # First check if the todo belongs to the current user
    existing_todo = get_todo_by_id_and_user(session, todo_id, current_user.id)
    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    return update_todo(session, existing_todo, todo_update)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_item(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a todo"""
    # First check if the todo belongs to the current user
    existing_todo = get_todo_by_id_and_user(session, todo_id, current_user.id)
    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    delete_todo(session, existing_todo)
    return

@router.patch("/{todo_id}/toggle-complete", response_model=dict)
def toggle_todo_complete(
    todo_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a todo"""
    # First check if the todo belongs to the current user
    existing_todo = get_todo_by_id_and_user(session, todo_id, current_user.id)
    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    updated_todo = toggle_todo_completion(session, existing_todo)
    return {"completed": updated_todo.completed}