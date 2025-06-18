from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./mindease.db")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai")  # openai or anthropic
    
    # Redis (for session management)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # App Settings
    APP_NAME: str = "MindEase"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Crisis Detection
    CRISIS_KEYWORDS: list = [
        "suicide", "kill myself", "want to die", "end it all",
        "self-harm", "cut myself", "hurt myself", "no reason to live"
    ]
    
    # Emergency Resources
    CRISIS_HOTLINE: str = "988"  # US National Suicide Prevention Lifeline
    CRISIS_TEXT: str = "Text HOME to 741741"  # Crisis Text Line
    
    class Config:
        env_file = ".env"

settings = Settings() 