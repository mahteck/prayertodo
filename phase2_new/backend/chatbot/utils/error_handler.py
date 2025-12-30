"""
Error Handler Utility
Formats user-friendly error messages in multiple languages
"""

import json
import os
from typing import Dict


def load_error_messages() -> Dict:
    """
    Load error message templates from JSON file

    Returns:
        Dict of error templates
    """
    # Get path to error_messages.json
    current_dir = os.path.dirname(__file__)
    config_dir = os.path.join(current_dir, '..', 'config')
    json_path = os.path.join(config_dir, 'error_messages.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Load error messages at module level
ERROR_MESSAGES = load_error_messages()


def format_error(error_code: str, language: str, **kwargs) -> str:
    """
    Format a user-friendly error message

    Args:
        error_code: Error code (e.g., "masjid_not_found")
        language: "en" or "ur"
        **kwargs: Placeholder values (name, area, count, input, etc.)

    Returns:
        Formatted error message string

    Examples:
        >>> msg = format_error("masjid_not_found", "en", name="Test Masjid")
        >>> "Test Masjid" in msg
        True
        >>> msg = format_error("backend_error", "ur")
        >>> "error" in msg.lower()
        True
    """
    # Default to backend_error if code not found
    if error_code not in ERROR_MESSAGES:
        error_code = "backend_error"

    # Get message template for language
    template = ERROR_MESSAGES[error_code].get(
        language,
        ERROR_MESSAGES[error_code].get("en")  # Fallback to English
    )

    # Replace placeholders
    for key, value in kwargs.items():
        placeholder = f"{{{key}}}"
        template = template.replace(placeholder, str(value))

    return template
