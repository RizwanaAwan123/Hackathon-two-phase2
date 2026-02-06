#!/bin/bash
# Script to run the complete Todo application with AI chatbot

echo "Starting Todo App with AI Chatbot..."

# Start the backend server in the background
echo "Starting backend server on port 8000..."
cd hackathonphase3/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!
cd ../..

# Give the backend a moment to start
sleep 3

# Check if backend started successfully
if ps -p $BACKEND_PID > /dev/null; then
    echo "Backend server is running with PID: $BACKEND_PID"

    # Start the frontend server
    echo "Starting frontend server on port 3000..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!

    echo "Frontend server is running with PID: $FRONTEND_PID"

    echo ""
    echo "==============================================="
    echo "Application is running!"
    echo ""
    echo "Frontend: http://localhost:3000"
    echo "Chat Dashboard: http://localhost:3000/chat-dashboard"
    echo "Backend API: http://localhost:8000"
    echo "Health Check: http://localhost:8000/health"
    echo ""
    echo "Press Ctrl+C to stop both servers"
    echo "==============================================="

    # Wait for both processes
    wait $BACKEND_PID $FRONTEND_PID
else
    echo "Failed to start backend server"
    exit 1
fi