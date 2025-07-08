# apis/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Agentic AI Translation System"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Agent Configuration
    MAX_TRANSLATION_LENGTH: int = 10000
    BATCH_SIZE_LIMIT: int = 50
    
    # Redis Configuration (for caching)
    REDIS_URL: str = "redis://localhost:6379"
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["pdf", "txt", "doc", "docx"]
    
    # Agent Timeouts
    AGENT_TIMEOUT: int = 30
    
    class Config:
        env_file = ".env"

# Create global settings instance
settings = Settings()