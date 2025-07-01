"""
Application configuration and settings.
"""
import os
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Coffee Shop API"
    
    # Database
    DATABASE_URL: str
    
    # Clerk Authentication
    CLERK_SECRET_KEY: str
    CLERK_JWT_VERIFICATION_KEY: Optional[str] = None
    CLERK_ISSUER: str = Field(default="https://clerk.com", alias="CLERK_JWT_ISSUER")
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174,http://localhost:5175"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_file_encoding="utf-8",
        extra="ignore"  # Allow extra fields in .env file
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS as a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Create global settings instance
settings = Settings()