import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"
    openai_temperature: float = 0.7
    
    # Database Configuration
    database_url: str
    
    # Application Settings
    app_name: str = "AI Appointment Chatbot"
    debug: bool = False
    
    # Conversation Settings
    max_conversation_history: int = 10
    session_timeout_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
