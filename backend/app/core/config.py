"""Configuration settings for the application."""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Poker Hand Evaluator API"
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@db:5432/poker"
    )
    
    class Config:
        """Pydantic config."""
        
        env_file = ".env"


settings = Settings() 