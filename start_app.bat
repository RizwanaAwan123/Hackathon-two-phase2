@echo off
REM Batch script to run the integrated Todo application with AI chatbot (Phase 2 + Phase 3)

echo Starting Integrated Todo App with AI Chatbot (Phase 2 + Phase 3)...

REM Start the backend server in the background
echo Starting backend server on port 8000...
cd backend

REM Run uvicorn in background
start /B cmd /c python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload

REM Give the backend a moment to start
timeout /t 5 /nobreak >nul

REM Start the frontend server
echo Starting frontend server on port 3000...
cd ../frontend

REM Run next dev in background
start /B cmd /c npm run dev

echo.
echo ===============================================
echo Application is running!
echo.
echo Frontend: http://localhost:3000
echo Chat Dashboard: http://localhost:3000/chat-dashboard
echo Backend API: http://localhost:8000
echo Health Check: http://localhost:8000/health
echo.
echo Servers are running in background windows
echo ===============================================
echo.
echo To stop the servers, close the respective command windows
echo or run: taskkill /IM python.exe /F and taskkill /IM node.exe /F
