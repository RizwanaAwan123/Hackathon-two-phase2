# Quickstart Guide for Phase II Todo Application

## Prerequisites
- Python 3.11+
- Node.js 18+
- Neon PostgreSQL account and database connection string
- Better Auth account or self-hosted instance

## Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `SECRET_KEY`: A secure secret key for JWT signing
6. Run database migrations: `python -m src.database.migrate`
7. Start the backend: `uvicorn src.api.main:app --reload --port 8000`

## Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Set up environment variables:
   - `NEXT_PUBLIC_API_URL`: Base URL for your backend API (e.g., http://localhost:8000)
4. Start the development server: `npm run dev`

## Initial Configuration
1. Access the application at http://localhost:3000
2. Create an account using the signup form
3. Verify account if required by Better Auth configuration
4. Sign in with your credentials
5. Begin adding todos through the UI

## Development Commands
- Backend tests: `pytest`
- Frontend tests: `npm run test`
- Backend linting: `flake8 src/`
- Frontend linting: `npm run lint`
- Database migrations: `python -m alembic upgrade head`