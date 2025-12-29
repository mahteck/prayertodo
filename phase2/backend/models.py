"""
SalaatFlow Phase II - Data Models

SQLModel models for spiritual tasks, masjids, and daily hadith.
These models serve as both Pydantic schemas and SQLAlchemy ORM models.
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship


# ============================================================================
# Enums
# ============================================================================

class TaskCategory(str, Enum):
    """Categories of spiritual tasks based on Islamic terminology"""
    FARZ = "Farz"      # Obligatory acts (فرض)
    SUNNAH = "Sunnah"  # Practices of Prophet Muhammad (ﷺ) (سنّة)
    NAFL = "Nafl"      # Voluntary worship acts (نفل)
    DEED = "Deed"      # General good deeds (charity, helping others)
    OTHER = "Other"    # Miscellaneous


class Priority(str, Enum):
    """Task priority levels"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"


class Recurrence(str, Enum):
    """Task recurrence patterns"""
    NONE = "None"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"


# ============================================================================
# SpiritualTask Model
# ============================================================================

class SpiritualTask(SQLModel, table=True):
    """
    Represents a spiritual task or religious obligation.

    Fields:
        id: Auto-incrementing primary key
        title: Task name (max 200 chars, indexed)
        description: Optional detailed description (max 2000 chars)
        category: TaskCategory enum (Farz, Sunnah, Nafl, Deed, Other)
        priority: Priority level (Low, Medium, High, Urgent)
        tags: JSON array of tags as comma-separated string
        masjid_id: Foreign key to Masjid table (optional)
        due_datetime: Optional deadline with time (indexed)
        recurrence: Recurrence pattern (None, Daily, Weekly, Monthly)
        completed: Completion status (boolean, indexed)
        created_at: Creation timestamp
        updated_at: Last modification timestamp
    """
    __tablename__ = "spiritual_tasks"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core fields
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=2000)

    # Categorization
    category: TaskCategory = Field(default=TaskCategory.OTHER)
    priority: Priority = Field(default=Priority.MEDIUM, index=True)
    tags: Optional[str] = Field(default=None)  # JSON array stored as comma-separated

    # Masjid relationship
    masjid_id: Optional[int] = Field(default=None, foreign_key="masjids.id")
    masjid: Optional["Masjid"] = Relationship(back_populates="tasks")

    # Scheduling
    due_datetime: Optional[datetime] = Field(default=None, index=True)
    recurrence: Recurrence = Field(default=Recurrence.NONE)

    # Status
    completed: bool = Field(default=False, index=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Masjid Model
# ============================================================================

class Masjid(SQLModel, table=True):
    """
    Represents a mosque with location and contact information.

    Fields:
        id: Auto-incrementing primary key
        name: Masjid name (max 200 chars, indexed, unique)
        area: Locality/neighborhood (max 200 chars, indexed)
        city: City name (max 100 chars)
        address: Full street address (max 500 chars)
        imam_name: Name of imam (max 200 chars)
        phone: Contact phone number (max 20 chars)
        created_at: Creation timestamp
        updated_at: Last modification timestamp
    """
    __tablename__ = "masjids"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core fields
    name: str = Field(max_length=200, index=True, unique=True)
    area: str = Field(max_length=200, index=True)
    city: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=500)

    # Contact information
    imam_name: Optional[str] = Field(default=None, max_length=200)
    phone: Optional[str] = Field(default=None, max_length=20)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["SpiritualTask"] = Relationship(back_populates="masjid")


# ============================================================================
# DailyHadith Model
# ============================================================================

class DailyHadith(SQLModel, table=True):
    """
    Represents a hadith of the day with Arabic text and translation.

    Fields:
        id: Auto-incrementing primary key
        date: Date for this hadith (indexed, unique)
        arabic_text: Hadith in Arabic (max 2000 chars)
        english_translation: English translation (max 2000 chars)
        reference: Source reference (e.g., "Sahih Bukhari 1234") (max 200 chars)
        narrator: Name of narrator (max 200 chars)
        created_at: Creation timestamp
    """
    __tablename__ = "daily_hadith"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Date (unique constraint - one hadith per day)
    date: datetime = Field(index=True, unique=True)

    # Content
    arabic_text: str = Field(max_length=2000)
    english_translation: str = Field(max_length=2000)
    reference: str = Field(max_length=200)  # e.g., "Sahih Bukhari 1234"
    narrator: Optional[str] = Field(default=None, max_length=200)

    # Timestamp
    created_at: datetime = Field(default_factory=datetime.utcnow)
