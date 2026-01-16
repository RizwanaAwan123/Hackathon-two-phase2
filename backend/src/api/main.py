from fastapi import FastAPI
from .auth_routes import router as auth_router
from .todo_routes import router as todo_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Todo API",
    description="API for managing todos with user authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(todo_router, prefix="/api/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)