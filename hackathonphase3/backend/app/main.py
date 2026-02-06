"""
Main application file for the AI Todo Chatbot.
This file sets up the FastAPI application and includes the API routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.core.config import settings

# Create the FastAPI application
app = FastAPI(
    title="AI Todo Chatbot API",
    description="An AI-powered conversational Todo chatbot with natural language processing capabilities",
    version="1.0.0"
)

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat router
app.include_router(chat_router, prefix="/api")

@app.get("/")
def read_root():
    """
    Root endpoint for health check.

    Returns:
        A simple message indicating the API is running
    """
    return {"message": "AI Todo Chatbot API is running!"}

@app.get("/health")
def health_check():
    """
    Health check endpoint.

    Returns:
        A dictionary with status and message
    """
    return {
        "status": "healthy",
        "message": "AI Todo Chatbot API is operational",
        "environment": settings.ENVIRONMENT
    }

# This would be the entry point when running uvicorn
# Example: uvicorn app.main:app --reload