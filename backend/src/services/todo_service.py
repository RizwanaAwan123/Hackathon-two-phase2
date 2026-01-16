from sqlmodel import Session, select
from typing import List, Optional
from ..models.todo import Todo, TodoCreate, TodoUpdate
from uuid import UUID

def create_todo_for_user(session: Session, todo: TodoCreate, user_id: UUID) -> Todo:
    """Create a new todo for a specific user"""
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=user_id
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

def get_todos_by_user(session: Session, user_id: UUID) -> List[Todo]:
    """Get all todos for a specific user"""
    statement = select(Todo).where(Todo.user_id == user_id)
    todos = session.exec(statement).all()
    return todos

def get_todo_by_id_and_user(session: Session, todo_id: str, user_id: UUID) -> Optional[Todo]:
    """Get a specific todo by ID and user ID to ensure ownership"""
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.exec(statement).first()
    return todo

def update_todo(session: Session, todo: Todo, todo_update: TodoUpdate) -> Todo:
    """Update an existing todo"""
    for field, value in todo_update.dict(exclude_unset=True).items():
        setattr(todo, field, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

def delete_todo(session: Session, todo: Todo) -> None:
    """Delete a todo"""
    session.delete(todo)
    session.commit()

def toggle_todo_completion(session: Session, todo: Todo) -> Todo:
    """Toggle the completion status of a todo"""
    todo.completed = not todo.completed
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo