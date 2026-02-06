"""
MCP Tool Server for the AI Todo Chatbot application.
This server exposes the task operations as MCP tools for the OpenAI Agent.
"""

from typing import Dict, Any, Optional
from app.mcp_tools.task_operations import (
    add_task,
    list_tasks,
    update_task,
    complete_task,
    delete_task
)

class MCPTaskTools:
    """
    Class containing MCP tools for task operations.

    These tools are meant to be used by the OpenAI Agent to perform
    operations on tasks in the database.
    """

    @staticmethod
    def add_task_tool(content: str, user_id: int, conversation_id: int) -> Dict[str, Any]:
        """
        MCP tool to add a new task.

        Args:
            content: The content of the task
            user_id: The ID of the user creating the task
            conversation_id: The ID of the conversation where task was created

        Returns:
            Result of the add_task operation
        """
        return add_task(content, user_id, conversation_id)

    @staticmethod
    def list_tasks_tool(user_id: int, status_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        MCP tool to list tasks for a user.

        Args:
            user_id: The ID of the user whose tasks to list
            status_filter: Optional status to filter by ('pending', 'completed')

        Returns:
            Result of the list_tasks operation
        """
        return list_tasks(user_id, status_filter)

    @staticmethod
    def update_task_tool(task_id: int, content: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
        """
        MCP tool to update an existing task.

        Args:
            task_id: The ID of the task to update
            content: New content for the task (optional)
            status: New status for the task (optional)

        Returns:
            Result of the update_task operation
        """
        return update_task(task_id, content, status)

    @staticmethod
    def complete_task_tool(task_id: int) -> Dict[str, Any]:
        """
        MCP tool to mark a task as completed.

        Args:
            task_id: The ID of the task to complete

        Returns:
            Result of the complete_task operation
        """
        return complete_task(task_id)

    @staticmethod
    def delete_task_tool(task_id: int) -> Dict[str, Any]:
        """
        MCP tool to delete a task.

        Args:
            task_id: The ID of the task to delete

        Returns:
            Result of the delete_task operation
        """
        return delete_task(task_id)

# Create an instance of the tools
mcp_task_tools = MCPTaskTools()