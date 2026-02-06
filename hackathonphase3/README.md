# AI-Powered Todo Chatbot

An AI-powered conversational Todo chatbot with natural language processing capabilities using MCP architecture, FastAPI backend, OpenAI Agents SDK, and Neon Serverless PostgreSQL.

## System Architecture

The system consists of the following components:

1. **Frontend**: Built with Next.js and React, provides a chat interface for users to interact with the AI agent
2. **Backend**: FastAPI application handling API requests and orchestrating the AI agent
3. **AI Agent**: OpenAI Agent configured with custom tools to perform todo operations
4. **MCP Tools**: Functions exposed to the AI agent for database operations
5. **Database**: PostgreSQL database storing tasks, conversations, and messages
6. **ORM**: SQLModel for database interactions

## How the System Works

1. **User Interaction**: The user sends a message through the frontend chat interface
2. **API Request**: The frontend sends the message to the backend `/api/{user_id}/chat` endpoint
3. **Conversation Management**: The system either creates a new conversation or continues an existing one
4. **Message Storage**: The user's message is stored in the database
5. **AI Processing**: An OpenAI agent processes the message and determines which tools to call
6. **Tool Execution**: The agent calls MCP tools (add_task, list_tasks, etc.) based on user intent
7. **Database Operations**: MCP tools perform operations on the database (CRUD operations on tasks)
8. **Response Generation**: The agent generates a natural language response based on tool results
9. **Response Storage**: The AI's response is stored in the database
10. **Return Response**: The response is sent back to the frontend for display

## Key Features

- **Natural Language Processing**: Users can interact using natural language
- **Task Operations**: Add, list, update, complete, and delete tasks
- **Confirmation System**: Destructive operations require confirmation
- **Conversation Context**: Maintains context across multiple interactions
- **Stateless Architecture**: Each request contains all necessary information
- **Error Handling**: Graceful handling of various error scenarios

## File Structure

```
project-root/
├── backend/
│   ├── app/
│   │   ├── models/           # SQLModel database models
│   │   │   ├── task.py
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   ├── mcp_tools/       # MCP server tools
│   │   │   ├── task_operations.py
│   │   │   └── tool_server.py
│   │   ├── api/             # API routes
│   │   │   └── chat.py
│   │   ├── agents/          # OpenAI Agent configuration
│   │   │   └── todo_agent.py
│   │   ├── database/        # Database session and config
│   │   │   └── session.py
│   │   ├── core/            # Core configurations
│   │   │   └── config.py
│   │   └── main.py          # Application entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── pages/
│   │       └── index.js     # Main chat interface
│   ├── package.json
│   └── public/
├── specs/
└── .env.example
```

## Setup Instructions

1. Clone the repository
2. Set up the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```
4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Update .env with your configuration
   ```
5. Run the applications:
   ```bash
   # Backend
   cd backend
   uvicorn app.main:app --reload

   # Frontend
   cd frontend
   npm run dev
   ```

## Environment Variables

- `DATABASE_URL`: PostgreSQL database connection string
- `OPENAI_API_KEY`: OpenAI API key for the AI agent
- `BETTER_AUTH_SECRET`: Secret for authentication (placeholder)
- `BETTER_AUTH_URL`: Authentication service URL (placeholder)
- `ENVIRONMENT`: Environment name (development, production)
- `LOG_LEVEL`: Logging level (info, debug, error)