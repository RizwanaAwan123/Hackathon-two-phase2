# Todo Application - Phase II

This is a full-stack todo application with user authentication, data persistence, and responsive UI. The system uses a Python REST API backend with Neon Serverless PostgreSQL, and a Next.js frontend with authentication for user management.

## Features

- User authentication (signup/signin)
- Todo management (create, read, update, delete)
- Todo completion toggling
- User-specific data isolation
- Responsive UI for desktop and mobile

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- SQLModel
- Neon Serverless PostgreSQL
- JWT-based authentication

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `SECRET_KEY`: A secure secret key for JWT signing
6. Run database migrations: `alembic upgrade head`
7. Start the backend: `uvicorn src.api.main:app --reload --port 8000`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Set up environment variables:
   - `NEXT_PUBLIC_API_URL`: Base URL for your backend API (e.g., http://localhost:8000)
4. Start the development server: `npm run dev`

## Environment Variables

### Backend (.env file in backend directory)
```
DATABASE_URL=postgresql://user:password@localhost/todo_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local file in frontend directory)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create a new user account
- `POST /api/auth/signin` - Authenticate a user
- `POST /api/auth/signout` - End user session

### Todos
- `GET /api/todos` - Get all todos for the authenticated user
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/{todo_id}` - Update an existing todo
- `DELETE /api/todos/{todo_id}` - Delete a todo
- `PATCH /api/todos/{todo_id}/toggle-complete` - Toggle todo completion status

## Project Structure

```
todo-phase2/
├── backend/
│   ├── src/
│   │   ├── models/      # Data models
│   │   ├── services/    # Business logic
│   │   ├── api/         # API routes
│   │   ├── database/    # Database configuration
│   │   └── config/      # Configuration settings
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Next.js pages
│   │   ├── services/    # API services
│   │   ├── hooks/       # Custom React hooks
│   │   └── types/       # TypeScript types
│   ├── package.json
│   └── next.config.js
└── specs/              # Specification files
    └── 002-phase2-todo-app/
```

## Development

This project follows the Spec-Driven Development (SDD) methodology with the following phases:
1. Specification (specs/)
2. Planning (plan.md)
3. Task breakdown (tasks.md)
4. Implementation

All changes should be made following this structured approach to ensure consistency and maintainability.