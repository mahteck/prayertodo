"""
Chatbot Configuration Settings
Loads Phase III environment variables for AI-powered features
Now using Google Gemini (FREE!)
"""

import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from backend directory
backend_dir = Path(__file__).parent.parent.parent
env_path = backend_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Required settings - Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable is required for Phase III chatbot functionality. "
        "Please set it in your .env file. Get your FREE API key from: https://aistudio.google.com/app/apikey"
    )

# Backend integration
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")

# Agent configuration
CHATBOT_MODEL = os.getenv("CHATBOT_MODEL", "gemini-1.5-flash")  # Free Gemini model
CHATBOT_TEMPERATURE = float(os.getenv("CHATBOT_TEMPERATURE", "0.7"))
CHATBOT_MAX_TOKENS = int(os.getenv("CHATBOT_MAX_TOKENS", "1000"))
CHATBOT_TIMEOUT = int(os.getenv("CHATBOT_TIMEOUT", "30"))

# User preferences (optional defaults)
DEFAULT_AREA: Optional[str] = os.getenv("DEFAULT_AREA")
DEFAULT_MASJID_ID: Optional[int] = int(os.getenv("DEFAULT_MASJID_ID")) if os.getenv("DEFAULT_MASJID_ID") else None

# Validation
print(f"✅ Chatbot settings loaded (Google Gemini):")
print(f"   Model: {CHATBOT_MODEL}")
print(f"   Backend: {BACKEND_BASE_URL}")
print(f"   API Key: {'Set ✅' if GEMINI_API_KEY else 'Missing ❌'}")
