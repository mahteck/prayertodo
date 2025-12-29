"""
Data models and type definitions for spiritual tasks.

This module defines the Task structure and category constants
for the SalaatFlow prayer and spiritual task management system.
"""

from datetime import datetime
from typing import TypedDict, Optional


# Category constants
CATEGORY_FARZ = "Farz"
CATEGORY_SUNNAH = "Sunnah"
CATEGORY_NAFL = "Nafl"
CATEGORY_DEED = "Deed"

CATEGORIES = [CATEGORY_FARZ, CATEGORY_SUNNAH, CATEGORY_NAFL, CATEGORY_DEED]


class Task(TypedDict):
    """
    Spiritual Task entity.

    Represents a prayer obligation, good deed, or spiritual reminder.
    """
    id: int
    title: str
    description: str
    category: str
    masjid_name: str
    area_name: str
    due_datetime: Optional[datetime]
    completed: bool
    created_at: datetime
    updated_at: datetime
