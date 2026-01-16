from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///./todo.db"

    # Auth settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Better Auth settings
    BETTER_AUTH_SECRET: str = "your-better-auth-secret-here"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()