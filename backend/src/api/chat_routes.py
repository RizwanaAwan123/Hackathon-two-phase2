from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
from uuid import UUID
import re

from ..middleware.auth import get_current_user
from ..models.user import User
from ..database.database import get_session
from ..services.todo_service import (
    create_todo_for_user,
    get_todos_by_user,
    get_todo_by_id_and_user,
    update_todo,
    delete_todo,
    toggle_todo_completion
)
from ..models.todo import TodoCreate, TodoUpdate

router = APIRouter(prefix="/api", tags=["chat"])

def process_chat_message(message: str, user_id: UUID, session):
    """
    Process chat message and perform todo operations based on natural language.

    Args:
        message: The user's input message
        user_id: The ID of the user
        session: Database session

    Returns:
        String response to the user
    """
    message_lower = message.lower().strip()

    # Handle adding a task
    if any(word in message_lower for word in ["add ", "add a task", "create", "new task", "make a task", "add task"]):
        # Extract task content by removing the command words
        content = message_lower.replace("add a task to ", "").replace("add ", "").replace("a task to ", "").replace("create ", "").replace("new task ", "").replace("make a task to ", "").replace("make ", "").strip()
        if content:
            # Create the todo
            todo_create = TodoCreate(title=content, description="", completed=False)
            new_todo = create_todo_for_user(session, todo_create, user_id)
            return f"✅ Task added. You can see it in your task list now. Task ID: {new_todo.id}"
        else:
            return "📝 Please specify what task you'd like to add. For example: 'Add a task to buy groceries'"

    # Handle showing/listing tasks
    elif any(word in message_lower for word in ["show", "list", "view", "display", "my tasks", "all tasks", "see tasks"]):
        todos = get_todos_by_user(session, user_id)
        if todos:
            task_list = "📋 Here are your tasks:\n"
            for todo in todos:
                status_emoji = "✅" if todo.completed else "⏳"
                task_list += f"\n{status_emoji} {todo.id}. {todo.title} ({'completed' if todo.completed else 'pending'})"
            return task_list
        else:
            return "📋 Your task list is empty. Would you like to add a task?"

    # Handle completing a task
    elif any(word in message_lower for word in ["complete", "done", "finish", "mark as done", "mark complete"]):
        # Extract task ID if mentioned
        task_ids = re.findall(r'\b\d+\b', message)
        if task_ids:
            task_id = task_ids[0]  # Get the first number found
            # Get the todo to make sure it belongs to the user
            todo = get_todo_by_id_and_user(session, task_id, user_id)
            if not todo:
                return f"❌ Task with ID {task_id} not found or doesn't belong to you."

            # Toggle completion
            updated_todo = toggle_todo_completion(session, todo)
            return f"✅ Task '{updated_todo.title}' marked as {'completed' if updated_todo.completed else 'pending'}. You can see it in your task list now."
        else:
            return "📝 Please specify which task to complete. For example: 'Mark task 1 as complete'"

    # Handle deleting a task
    elif any(word in message_lower for word in ["delete", "remove", "erase", "cancel", "remove task"]):
        # Extract task ID if mentioned
        task_ids = re.findall(r'\b\d+\b', message)
        if task_ids:
            task_id = task_ids[0]  # Get the first number found
            # Get the todo to make sure it belongs to the user
            todo = get_todo_by_id_and_user(session, task_id, user_id)
            if not todo:
                return f"❌ Task with ID {task_id} not found or doesn't belong to you."

            # Delete the todo
            delete_todo(session, todo)
            return f"🗑️ Task '{todo.title}' deleted. You can see the changes in your task list now."
        else:
            return "📝 Please specify which task to delete. For example: 'Delete task 1'"

    # Handle updating a task
    elif any(word in message_lower for word in ["update", "change", "modify", "edit", "rename"]):
        # This is more complex - we'll need to extract task ID and new content
        task_ids = re.findall(r'\b\d+\b', message)
        if task_ids:
            task_id = task_ids[0]  # Get the first number found
            # Get the todo to make sure it belongs to the user
            todo = get_todo_by_id_and_user(session, task_id, user_id)
            if not todo:
                return f"❌ Task with ID {task_id} not found or doesn't belong to you."

            # Extract new content (anything after "to" or "as" or after the task number)
            match = re.search(r'(?:to|as|:)\s*(.+)', message, re.IGNORECASE)
            if match:
                new_content = match.group(1).strip()
                # Update the todo
                todo_update = TodoUpdate(title=new_content)
                updated_todo = update_todo(session, todo, todo_update)
                return f"📝 Task updated to '{updated_todo.title}'. You can see the changes in your task list now."
            else:
                return "📝 Please specify what to update the task to. For example: 'Update task 1 to buy milk'"
        else:
            return "📝 Please specify which task to update and what to change it to. For example: 'Update task 1 to buy milk'"

    # Default response for unrecognized commands
    else:
        return "👋 Hi! I'm your AI Task Assistant. I can help you add, view, complete, or delete tasks. What would you like to do today? 😊\n\nExamples:\n• 'Add a task to buy groceries'\n• 'Show my tasks'\n• 'Mark task 1 as complete'\n• 'Delete task 1'"

@router.post("/chat")
async def chat_endpoint(
    message_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """
    Chat endpoint that processes natural language commands to manage todos.
    Uses the same backend services as the UI to ensure consistency.

    Args:
        message_data: Dictionary containing 'message' and optional 'conversation_id'
        current_user: The authenticated user from the JWT token

    Returns:
        Response with AI-generated message
    """
    try:
        # Extract message from the request
        user_message = message_data.get("message")

        if not user_message:
            raise HTTPException(status_code=400, detail="Message content is required")

        # Get database session
        session_gen = get_session()
        session = next(session_gen)

        try:
            # Process the message and perform the appropriate action
            response = process_chat_message(user_message, current_user.id, session)

            # Return the response
            return {
                "response": response,
                "status": "success"
            }
        finally:
            session.close()

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error in a real application
        print(f"Chat processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/chat/test")
async def test_chat_endpoint():
    """
    Test endpoint to verify the chat endpoint is working.
    """
    return {"status": "chat endpoint is working"}