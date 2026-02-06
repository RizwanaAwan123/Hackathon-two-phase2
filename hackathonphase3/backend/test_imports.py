import sys
import os
sys.path.insert(0, '.')

# Manually set environment variables for testing
os.environ['DATABASE_URL'] = 'sqlite:///./todo_chatbot.db'
os.environ['OPENAI_API_KEY'] = 'test-key'

from app.core.config import settings
print("Settings loaded successfully!")
print(f"Database URL: {settings.DATABASE_URL}")
print(f"Environment: {settings.ENVIRONMENT}")

# Test importing the database session
try:
    from app.database.session import engine
    print("Database engine created successfully!")
except Exception as e:
    print(f"Error creating database engine: {e}")

# Test importing the models
try:
    from app.models.task import Task
    print("Task model imported successfully!")
except Exception as e:
    print(f"Error importing Task model: {e}")

# Test importing the agent
try:
    from app.agents.todo_agent import TodoAgent
    print("TodoAgent imported successfully!")
except Exception as e:
    print(f"Error importing TodoAgent: {e}")

print("All imports successful!")