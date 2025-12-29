"""
SalaatFlow Phase II - Configuration Management

Environment-based configuration using Pydantic Settings.
Loads configuration from .env file and environment variables.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings can be overridden by environment variables.
    Create a .env file in the backend directory to set these values.
    """

    # Database Configuration
    database_url: str = ""

    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000

    # Environment
    environment: str = "development"

    # API Configuration
    api_v1_prefix: str = "/api/v1"
    app_name: str = "SalaatFlow API"
    app_version: str = "2.0.0"
    debug: bool = True

    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> List[str]:
        """
        Parse CORS origins from comma-separated string to list.

        Returns:
            List[str]: List of allowed CORS origins
        """
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        """
        Check if running in production environment.

        Returns:
            bool: True if environment is production
        """
        return self.environment.lower() == "production"


# Global settings instance
settings = Settings()


# Validate critical settings
if not settings.database_url:
    raise ValueError(
        "DATABASE_URL is not set. Please create a .env file with your database connection string.\n"
        "Copy .env.example to .env and fill in your Neon PostgreSQL credentials."
    )
