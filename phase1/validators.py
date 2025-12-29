"""
Input validation functions for task fields.

This module provides validation for all user inputs including
title, category, datetime, and ID fields.
"""

from datetime import datetime
from typing import Optional

# Import categories - will work when run as module or script
try:
    from models import CATEGORIES
except ImportError:
    from phase1.models import CATEGORIES


# Field length constants
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
MAX_MASJID_NAME_LENGTH = 100
MAX_AREA_NAME_LENGTH = 100
DATETIME_FORMAT = "YYYY-MM-DD HH:MM"


def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate task title.

    Args:
        title: The title string to validate

    Returns:
        Tuple of (is_valid, error_message)
        - (True, "") if valid
        - (False, error_message) if invalid
    """
    if not title or len(title.strip()) == 0:
        return (False, "Title cannot be empty")

    if len(title) > MAX_TITLE_LENGTH:
        return (False, f"Title must be {MAX_TITLE_LENGTH} characters or less")

    return (True, "")


def validate_category(choice: str) -> tuple[bool, str]:
    """
    Validate category choice.

    Args:
        choice: User input (expected "1", "2", "3", or "4")

    Returns:
        Tuple of (is_valid, category_name)
        - (True, category_name) if valid choice
        - (False, "") if invalid
    """
    category_map = {
        "1": CATEGORIES[0],  # Farz
        "2": CATEGORIES[1],  # Sunnah
        "3": CATEGORIES[2],  # Nafl
        "4": CATEGORIES[3],  # Deed
    }

    if choice in category_map:
        return (True, category_map[choice])

    return (False, "")


def validate_datetime(datetime_str: str) -> tuple[bool, Optional[datetime]]:
    """
    Validate datetime string in format YYYY-MM-DD HH:MM.

    Args:
        datetime_str: The datetime string to parse

    Returns:
        Tuple of (is_valid, datetime_object)
        - (True, datetime_obj) if valid
        - (False, None) if invalid
    """
    if not datetime_str or len(datetime_str.strip()) == 0:
        return (True, None)  # Empty is valid (optional field)

    try:
        # Parse format: YYYY-MM-DD HH:MM
        dt = datetime.strptime(datetime_str.strip(), "%Y-%m-%d %H:%M")
        return (True, dt)
    except ValueError:
        return (False, None)


def validate_id(id_str: str) -> tuple[bool, Optional[int]]:
    """
    Validate ID string is numeric.

    Args:
        id_str: The ID string to validate

    Returns:
        Tuple of (is_valid, id_int)
        - (True, id_int) if valid numeric
        - (False, None) if non-numeric
    """
    try:
        id_int = int(id_str)
        return (True, id_int)
    except (ValueError, TypeError):
        return (False, None)
