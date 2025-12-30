"""
Configuration settings for SalaatFlow API
Uses Pydantic Settings for environment variable management
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = "SalaatFlow API"
    app_version: str = "1.0.0"
    environment: str = "development"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str

    # CORS
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # API
    api_v1_prefix: str = "/api/v1"

    # Phase III - AI Chatbot Settings (Google Gemini)
    gemini_api_key: str = "your-gemini-api-key"
    backend_base_url: str = "http://localhost:8000"
    chatbot_model: str = "gemini-1.5-flash"
    chatbot_temperature: float = 0.7
    chatbot_max_tokens: int = 1000
    chatbot_timeout: int = 30
    default_area: str = "North Nazimabad"
    default_masjid_id: int = 1

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Create settings instance
settings = Settings()
