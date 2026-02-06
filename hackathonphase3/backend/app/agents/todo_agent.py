"""
Gemini Agent configuration for the AI Todo Chatbot application.
This agent uses the MCP tools to perform task operations based on natural language input.
"""

import os
from typing import Dict, Any, List
import google.generativeai as genai
from app.mcp_tools.tool_server import mcp_task_tools
from app.core.config import settings

# Don't initialize client at module level to avoid issues
client = None

# Define the tools available to the agent
TASK_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the user's todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The content of the task to add"
                    },
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user creating the task"
                    },
                    "conversation_id": {
                        "type": "integer",
                        "description": "The ID of the conversation where task was created"
                    }
                },
                "required": ["content", "user_id", "conversation_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks for a user, with optional status filter",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "integer",
                        "description": "The ID of the user whose tasks to list"
                    },
                    "status_filter": {
                        "type": "string",
                        "enum": ["pending", "completed"],
                        "description": "Optional status to filter tasks by"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "content": {
                        "type": "string",
                        "description": "New content for the task (optional)"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "completed"],
                        "description": "New status for the task (optional)"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to complete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]

class TodoAgent:
    """
    OpenAI Agent configured to handle todo operations using MCP tools.
    """

    def __init__(self, user_id: int, conversation_id: int):
        """
        Initialize the agent with user and conversation context.

        Args:
            user_id: The ID of the user interacting with the agent
            conversation_id: The ID of the current conversation
        """
        self.user_id = user_id
        self.conversation_id = conversation_id

        # Define function tools for Gemini
        def add_task(content: str, user_id: int, conversation_id: int):
            """Add a new task to the user's todo list"""
            return mcp_task_tools.add_task_tool(content=content, user_id=user_id, conversation_id=conversation_id)

        def list_tasks(user_id: int, status_filter: str = None):
            """List all tasks for a user, with optional status filter"""
            return mcp_task_tools.list_tasks_tool(user_id=user_id, status_filter=status_filter)

        def update_task(task_id: int, content: str = None, status: str = None):
            """Update an existing task"""
            return mcp_task_tools.update_task_tool(task_id=task_id, content=content, status=status)

        def complete_task(task_id: int):
            """Mark a task as completed"""
            return mcp_task_tools.complete_task_tool(task_id=task_id)

        def delete_task(task_id: int):
            """Delete a task"""
            return mcp_task_tools.delete_task_tool(task_id=task_id)

        self.tools = [add_task, list_tasks, update_task, complete_task, delete_task]

    def process_message(self, message: str) -> str:
        """
        Process a user message and return an appropriate response.

        Args:
            message: The user's input message

        Returns:
            The agent's response to the user
        """
        # Process the message using the actual tools regardless of API key presence
        message_lower = message.lower().strip()

        # Handle adding a task
        if any(word in message_lower for word in ["add ", "add a task", "create", "new task", "make a task"]):
            # Extract task content by removing the command words
            content = message_lower.replace("add ", "").replace("a task to ", "").replace("create ", "").replace("new task ", "").strip()
            if content:
                result = mcp_task_tools.add_task_tool(content=content, user_id=self.user_id, conversation_id=self.conversation_id)
                if result["success"]:
                    return f"✅ Got it! I've added '{content}' to your task list. Task ID: {result['task_id']}"
                else:
                    return f"❌ Sorry, I couldn't add the task: {result['message']}"
            else:
                return "📝 Please specify what task you'd like to add. For example: 'Add a task to buy groceries'"

        # Handle showing/listing tasks
        elif any(word in message_lower for word in ["show", "list", "view", "display", "my tasks", "all tasks"]):
            status_filter = None
            if "completed" in message_lower:
                status_filter = "completed"
            elif "pending" in message_lower or "incomplete" in message_lower:
                status_filter = "pending"

            result = mcp_task_tools.list_tasks_tool(user_id=self.user_id, status_filter=status_filter)
            if result["success"]:
                tasks = result["tasks"]
                if tasks:
                    if status_filter:
                        task_list = f"📋 Here are your {status_filter} tasks:\n"
                    else:
                        task_list = "📋 Here are your tasks:\n"

                    for task in tasks:
                        status_emoji = "✅" if task["status"] == "completed" else "⏳"
                        task_list += f"\n{status_emoji} {task['id']}. {task['content']} ({task['status']})"
                    return task_list
                else:
                    if status_filter:
                        return f"📋 You don't have any {status_filter} tasks right now."
                    else:
                        return "📋 Your task list is empty. Would you like to add a task?"
            else:
                return f"❌ Sorry, I couldn't retrieve your tasks: {result['message']}"

        # Handle completing a task
        elif any("complete" in message_lower or "done" in message_lower or "finish" in message_lower for word in ["complete", "done", "finish"]):
            # Extract task ID if mentioned
            import re
            task_ids = re.findall(r'\b\d+\b', message)
            if task_ids:
                task_id = int(task_ids[0])
                result = mcp_task_tools.complete_task_tool(task_id=task_id)
                if result["success"]:
                    return f"✅ Great! I've marked task {task_id} as completed."
                else:
                    return f"❌ Sorry, I couldn't complete the task: {result['message']}"
            else:
                return "📝 Please specify which task to complete. For example: 'Mark task 1 as complete'"

        # Handle deleting a task
        elif any(word in message_lower for word in ["delete", "remove", "erase", "cancel"]):
            # Extract task ID if mentioned
            import re
            task_ids = re.findall(r'\b\d+\b', message)
            if task_ids:
                task_id = int(task_ids[0])
                result = mcp_task_tools.delete_task_tool(task_id=task_id)
                if result["success"]:
                    return f"🗑️ Done! I've removed task {task_id} from your list."
                else:
                    return f"❌ Sorry, I couldn't delete the task: {result['message']}"
            else:
                return "📝 Please specify which task to delete. For example: 'Delete task 1'"

        # Handle updating a task
        elif any(word in message_lower for word in ["update", "change", "modify", "edit"]):
            # This is more complex - we'll need to extract task ID and new content
            import re
            task_ids = re.findall(r'\b\d+\b', message)
            if task_ids:
                task_id = int(task_ids[0])
                # Extract new content (anything after "to" or "as" or after the task number)
                import re
                # Look for patterns like "update task 1 to buy milk" or "change task 1 to buy milk"
                match = re.search(r'(?:to|as|:)\s*(.+)', message, re.IGNORECASE)
                if match:
                    new_content = match.group(1).strip()
                    result = mcp_task_tools.update_task_tool(task_id=task_id, content=new_content)
                    if result["success"]:
                        return f"📝 Updated! Task {task_id} is now '{new_content}'."
                    else:
                        return f"❌ Sorry, I couldn't update the task: {result['message']}"
                else:
                    return "📝 Please specify what to update the task to. For example: 'Update task 1 to buy milk'"
            else:
                return "📝 Please specify which task to update and what to change it to. For example: 'Update task 1 to buy milk'"

        # Default response for unrecognized commands
        else:
            return "👋 Hi! I'm your AI Task Assistant. I can help you add, view, complete, or delete tasks. What would you like to do today? 😊\n\nExamples:\n• 'Add a task to buy groceries'\n• 'Show my tasks'\n• 'Mark task 1 as complete'\n• 'Delete task 1'"

            # If we have a valid API key, initialize the Gemini client
            if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
                try:
                    genai.configure(api_key=settings.GEMINI_API_KEY)
                    self._model = genai.GenerativeModel('gemini-1.5-flash')
                except Exception:
                    return "Gemini API key is configured but client initialization failed."

        try:
            # Create a simple prompt for the chatbot
            prompt = f"""You are a helpful todo list assistant. You can help users manage their tasks.

Available actions:
- Add tasks: "add a task to buy groceries"
- List tasks: "show my tasks" or "list completed tasks"
- Update tasks: "change task 1 to buy milk"
- Complete tasks: "mark task 1 as done"
- Delete tasks: "delete task 1"

User message: {message}

Please respond helpfully and acknowledge what the user wants to do."""

            response = self._model.generate_content(prompt)

            if response.text:
                return response.text.strip()
            else:
                return "I understand you want to manage your tasks. How can I help you today?"

        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try again."

def create_todo_agent(user_id: int, conversation_id: int) -> TodoAgent:
    """
    Factory function to create a new TodoAgent instance.

    Args:
        user_id: The ID of the user
        conversation_id: The ID of the conversation

    Returns:
        A new TodoAgent instance
    """
    return TodoAgent(user_id, conversation_id)