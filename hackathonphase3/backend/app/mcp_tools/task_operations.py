"""
MCP tools for task operations in the AI Todo Chatbot application.
These tools are used by the OpenAI Agent to perform operations on tasks.
"""

from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from app.models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from app.models.conversation import Conversation
from app.database.session import engine

def add_task(content: str, user_id: int, conversation_id: int) -> Dict[str, Any]:
    """
    Add a new task to the database.

    Args:
        content: The content of the task
        user_id: The ID of the user creating the task
        conversation_id: The ID of the conversation where task was created

    Returns:
        Dictionary containing success status, task ID, and message
    """
    try:
        with Session(engine) as session:
            # Create a new task
            task = Task(
                content=content,
                user_id=user_id,
                conversation_id=conversation_id
            )

            # Add to database
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "task_id": task.id,
                "message": f"Successfully added task: '{content}'"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to add task: {str(e)}"
        }

def list_tasks(user_id: int, status_filter: Optional[str] = None) -> Dict[str, Any]:
    """
    List all tasks for a user, with optional status filtering.

    Args:
        user_id: The ID of the user whose tasks to list
        status_filter: Optional status to filter by ('pending', 'completed')

    Returns:
        Dictionary containing success status and list of tasks
    """
    try:
        with Session(engine) as session:
            # Build query based on filters
            query = select(Task).where(Task.user_id == user_id)

            if status_filter:
                if status_filter.lower() in ['pending', 'completed']:
                    query = query.where(Task.status == TaskStatus(status_filter.lower()))

            # Execute query
            tasks = session.exec(query).all()

            # Format response
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "content": task.content,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                })

            return {
                "success": True,
                "tasks": task_list
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to list tasks: {str(e)}"
        }

def update_task(task_id: int, content: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
    """
    Update an existing task.

    Args:
        task_id: The ID of the task to update
        content: New content for the task (optional)
        status: New status for the task (optional)

    Returns:
        Dictionary containing success status and message
    """
    try:
        with Session(engine) as session:
            # Get the task
            task = session.get(Task, task_id)

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found"
                }

            # Update fields if provided
            if content is not None:
                task.content = content

            if status is not None:
                if status.lower() in ['pending', 'completed']:
                    task.status = TaskStatus(status.lower())
                else:
                    return {
                        "success": False,
                        "message": f"Invalid status: {status}. Must be 'pending' or 'completed'"
                    }

            task.updated_at = task.updated_at  # This will update the timestamp

            # Save changes
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": f"Successfully updated task {task_id}"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to update task: {str(e)}"
        }

def complete_task(task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        task_id: The ID of the task to complete

    Returns:
        Dictionary containing success status and message
    """
    try:
        with Session(engine) as session:
            # Get the task
            task = session.get(Task, task_id)

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found"
                }

            # Update status to completed
            task.status = TaskStatus.completed
            task.updated_at = task.updated_at  # This will update the timestamp

            # Save changes
            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "message": f"Successfully completed task {task_id}: '{task.content}'"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to complete task: {str(e)}"
        }

def delete_task(task_id: int) -> Dict[str, Any]:
    """
    Delete a task from the database.

    Args:
        task_id: The ID of the task to delete

    Returns:
        Dictionary containing success status and message
    """
    try:
        with Session(engine) as session:
            # Get the task
            task = session.get(Task, task_id)

            if not task:
                return {
                    "success": False,
                    "message": f"Task with ID {task_id} not found"
                }

            # Delete the task
            session.delete(task)
            session.commit()

            return {
                "success": True,
                "message": f"Successfully deleted task {task_id}: '{task.content}'"
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to delete task: {str(e)}"
        }