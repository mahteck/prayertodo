"""
Gemini API Configuration Module

Provides validated configuration for Google Gemini API integration.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class GeminiConfig(BaseModel):
    """
    Configuration for Google Gemini API.

    Validates API key format and provides sensible defaults.
    """

    api_key: str = Field(..., description="Google Gemini API key")
    model: str = Field(default="gemini-2.0-flash", description="Gemini model name")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=2, description="Maximum retry attempts")
    retry_delay: float = Field(default=1.0, description="Delay between retries in seconds")

    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate Gemini API key format."""
        if not v:
            raise ValueError("GEMINI_API_KEY cannot be empty")

        # Check for placeholder values
        placeholder_values = [
            "your-gemini-api-key",
            "your-api-key-here",
            "placeholder",
            "xxx",
        ]
        if v.lower() in placeholder_values:
            raise ValueError(
                f"Invalid Gemini API key: '{v}' appears to be a placeholder. "
                "Please set a real API key from https://makersuite.google.com/app/apikey"
            )

        # Gemini API keys should start with "AIza"
        if not v.startswith("AIza"):
            raise ValueError(
                f"Invalid Gemini API key format. "
                f"Gemini API keys should start with 'AIza'. "
                f"Please verify your API key from https://makersuite.google.com/app/apikey"
            )

        # Check minimum length (Gemini keys are typically 39 characters)
        if len(v) < 35:
            raise ValueError(
                f"Invalid Gemini API key: too short (expected ~39 characters, got {len(v)}). "
                f"Please verify your API key."
            )

        return v

    @field_validator('timeout')
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        """Validate timeout is within reasonable range."""
        if not 5 <= v <= 300:
            raise ValueError(f"Timeout must be between 5 and 300 seconds, got {v}")
        return v

    @field_validator('max_retries')
    @classmethod
    def validate_max_retries(cls, v: int) -> int:
        """Validate max_retries is reasonable."""
        if not 0 <= v <= 5:
            raise ValueError(f"Max retries must be between 0 and 5, got {v}")
        return v

    @field_validator('retry_delay')
    @classmethod
    def validate_retry_delay(cls, v: float) -> float:
        """Validate retry_delay is reasonable."""
        if not 0.1 <= v <= 10.0:
            raise ValueError(f"Retry delay must be between 0.1 and 10.0 seconds, got {v}")
        return v

    @classmethod
    def from_env(cls) -> "GeminiConfig":
        """
        Load configuration from environment variables.

        Environment variables:
        - GEMINI_API_KEY (required)
        - GEMINI_MODEL (optional, default: gemini-1.5-flash)
        - GEMINI_TIMEOUT (optional, default: 30)
        - GEMINI_MAX_RETRIES (optional, default: 2)
        - GEMINI_RETRY_DELAY (optional, default: 1.0)

        Returns:
            GeminiConfig instance

        Raises:
            ValueError: If GEMINI_API_KEY is not set or invalid
        """
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please set it with your Google Gemini API key from "
                "https://makersuite.google.com/app/apikey"
            )

        return cls(
            api_key=api_key,
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            timeout=int(os.getenv("GEMINI_TIMEOUT", "30")),
            max_retries=int(os.getenv("GEMINI_MAX_RETRIES", "2")),
            retry_delay=float(os.getenv("GEMINI_RETRY_DELAY", "1.0")),
        )

    class Config:
        """Pydantic config."""
        frozen = True  # Make config immutable


# Singleton instance - loaded once at module import
_config: Optional[GeminiConfig] = None


def get_gemini_config() -> GeminiConfig:
    """
    Get the global Gemini configuration instance.

    Loads configuration from environment on first call,
    then returns cached instance.

    Returns:
        GeminiConfig instance

    Raises:
        ValueError: If configuration is invalid
    """
    global _config

    if _config is None:
        _config = GeminiConfig.from_env()

    return _config


# For testing - reset the singleton
def reset_config():
    """Reset the configuration singleton (for testing only)."""
    global _config
    _config = None


if __name__ == "__main__":
    """Test configuration loading."""
    import sys

    print("🔧 Testing Gemini Configuration...")
    print("=" * 60)

    try:
        config = GeminiConfig.from_env()

        print("✅ Configuration loaded successfully!")
        print(f"📊 Model: {config.model}")
        print(f"⏱️  Timeout: {config.timeout}s")
        print(f"🔄 Max Retries: {config.max_retries}")
        print(f"⏳ Retry Delay: {config.retry_delay}s")
        print(f"🔑 API Key: {config.api_key[:10]}...{config.api_key[-5:]}")

        print("\n" + "=" * 60)
        print("✅ All validation checks passed!")

        sys.exit(0)

    except ValueError as e:
        print(f"\n❌ Configuration Error:")
        print(f"   {str(e)}")
        print("\n" + "=" * 60)
        print("💡 Fix the issue and try again.")

        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Unexpected Error:")
        print(f"   {type(e).__name__}: {str(e)}")

        sys.exit(1)
