# Quickstart Guide: AI Todo Chatbot

## Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL-compatible database (Neon Serverless)
- OpenAI API key
- Better Auth account

## Setup Instructions

### 1. Clone and Initialize
```bash
git clone <repository-url>
cd ai-todo-chatbot
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Update .env with your configuration
```

### 3. Database Setup
```bash
# Set up Neon Serverless PostgreSQL
# Run migrations
alembic upgrade head
```

### 4. Environment Variables
Create `.env` file with:
```
DATABASE_URL=<your_neon_database_url>
OPENAI_API_KEY=<your_openai_api_key>
BETTER_AUTH_SECRET=<your_auth_secret>
BETTER_AUTH_URL=<your_auth_url>
```

### 5. Start Services
```bash
# Start MCP server
python -m mcp_tools.tool_server

# Start FastAPI backend
uvicorn app.main:app --reload

# Start frontend
cd ../frontend
npm install
npm run dev
```

## Architecture Overview

### Data Flow
1. User sends message via ChatKit frontend
2. Frontend calls backend chat endpoint
3. Backend authenticates user
4. Message stored in conversation history
5. OpenAI Agent processes message with available MCP tools
6. Agent invokes appropriate MCP tools for task operations
7. Tools interact with database to perform operations
8. Agent generates response based on tool results
9. Response stored and returned to frontend
10. Conversation continues with updated context

### Key Components
- **Models**: SQLModel classes for Task, Conversation, Message
- **MCP Tools**: Exposed functions for task operations
- **Agent**: OpenAI Agent configured with MCP tools
- **API**: Stateless chat endpoint handling requests
- **Database**: Neon PostgreSQL for data persistence