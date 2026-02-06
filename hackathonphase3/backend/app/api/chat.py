"""
Chat API endpoint for the AI Todo Chatbot application.
This endpoint handles user messages and returns AI-generated responses.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Dict, Any
from app.database.session import get_session
from app.agents.todo_agent import create_todo_agent
from app.models.message import Message
from app.models.conversation import Conversation

# Create router - routes will be absolute paths
router = APIRouter()

@router.post("/{user_id}/chat")
async def chat_endpoint(
    user_id: int,
    message_data: Dict[str, Any],
    session: Session = Depends(get_session)
) -> Dict[str, Any]:
    """
    Stateless chat endpoint that processes user messages and returns AI responses.

    Args:
        user_id: The ID of the user sending the message
        message_data: Dictionary containing 'message' and optional 'conversation_id'
        session: Database session for database operations

    Returns:
        Dictionary containing the AI response and conversation context
    """
    try:
        # Extract message and conversation_id from the request
        user_message = message_data.get("message")
        conversation_id = message_data.get("conversation_id")

        if not user_message:
            raise HTTPException(status_code=400, detail="Message content is required")

        # If no conversation_id is provided, create a new conversation
        if not conversation_id:
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            conversation_id = conversation.id
        else:
            # Verify that the conversation belongs to the user
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(status_code=404, detail="Conversation not found or unauthorized")

        # Create a message record for the user's input
        user_message_record = Message(
            role="user",
            content=user_message,
            conversation_id=conversation_id
        )
        session.add(user_message_record)
        session.commit()

        # Create the AI agent and process the message
        agent = create_todo_agent(user_id, conversation_id)
        ai_response = agent.process_message(user_message)

        # Create a message record for the AI's response
        ai_message_record = Message(
            role="assistant",
            content=ai_response,
            conversation_id=conversation_id
        )
        session.add(ai_message_record)
        session.commit()

        # Return the response
        return {
            "response": ai_response,
            "conversation_id": conversation_id,
            "timestamp": ai_message_record.timestamp.isoformat(),
            "status": "success"
        }

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error in a real application
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/chat")
async def legacy_chat_endpoint(
    message_data: Dict[str, Any]
):
    """
    Legacy chat endpoint that maintains compatibility with the Phase 2 frontend.
    This endpoint is for frontend compatibility - it returns a basic response.
    """
    try:
        user_message = message_data.get("message")

        if not user_message:
            raise HTTPException(status_code=400, detail="Message content is required")

        # Simple response to indicate the endpoint is working for frontend compatibility
        response = "👋 Hi! I'm your AI Task Assistant. The chat functionality is connected and working. In the full implementation, I would help you manage your tasks using natural language.\n\nTry commands like:\n• 'Add a task to buy groceries'\n• 'Show my tasks'\n• 'Mark task 1 as complete'\n• 'Delete task 2'"

        return {
            "response": response,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/chat/test")
async def test_chat_endpoint():
    """
    Test endpoint to verify the chat endpoint is working.
    """
    return {"status": "chat endpoint is working"}