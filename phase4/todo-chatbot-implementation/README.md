# TodoX Chatbot - Professional Todo Management Assistant

## Overview
A professional-grade Todo chatbot with advanced NLP capabilities that understands natural language commands.

## Features
- Natural language processing for todo management
- Add, list, complete, and delete tasks
- Professional chat interface
- Real-time responses
- Smart command recognition

## Commands Supported
- `add buy milk` or `add task buy milk` - Add a new task
- `show todos` or `list my tasks` - Show all tasks
- `complete 1` or `done 1` - Mark task as completed
- `delete 1` or `remove buy milk` - Delete task by ID or name
- `clear all todos` - Remove all tasks
- `help` - Show all available commands

## Architecture
- **Backend**: Node.js/Express server running on port 8000
- **Frontend**: Professional chat UI running on port 3000
- **API**: RESTful endpoints with enhanced chatbot processing

## Endpoints
- `POST /api/chat` - Chatbot command processing
- `GET /api/todos` - Get all todos
- `POST /api/todos` - Create a todo
- `PUT /api/todos/:id` - Update a todo
- `DELETE /api/todos/:id` - Delete a todo
- `GET /api/health` - Health check

## Running the Application
1. Start the backend: `cd backend && node server.js`
2. Start the frontend: `cd frontend && npx http-server -p 3000`
3. Access the UI at: `http://localhost:3000`
4. API available at: `http://localhost:8000`

## Technology Stack
- Node.js/Express for backend
- HTML/CSS/JavaScript for frontend
- Strong rule-based NLP for command processing
- Professional chat UI with animations