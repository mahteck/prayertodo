"""
Database models for SalaatFlow
Uses SQLModel (combines SQLAlchemy + Pydantic)
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


# Enums for task categorization
class TaskCategory(str, Enum):
    """Islamic categories for spiritual tasks"""
    FARZ = "Farz"  # Obligatory
    SUNNAH = "Sunnah"  # Prophetic tradition
    NAFL = "Nafl"  # Voluntary
    DEED = "Deed"  # Good deeds
    OTHER = "Other"


class Priority(str, Enum):
    """Task priority levels"""
    URGENT = "Urgent"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Recurrence(str, Enum):
    """Task recurrence patterns"""
    NONE = "None"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"


# Database Models
class Masjid(SQLModel, table=True):
    """Masjid (Mosque) model for location-based tasks"""
    __tablename__ = "masjids"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200, index=True)
    area_name: str = Field(max_length=100, index=True)  # Required for filtering
    city: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=500)
    imam_name: Optional[str] = Field(default=None, max_length=200)
    phone: Optional[str] = Field(default=None, max_length=20)

    # Geographic coordinates (optional, for future map features)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)

    # Prayer Times (HH:MM format) - Required for 5 daily prayers
    fajr_time: str = Field(max_length=5)  # e.g., "05:30"
    dhuhr_time: str = Field(max_length=5)  # e.g., "13:00"
    asr_time: str = Field(max_length=5)  # e.g., "16:30"
    maghrib_time: str = Field(max_length=5)  # e.g., "18:15"
    isha_time: str = Field(max_length=5)  # e.g., "19:45"
    jummah_time: Optional[str] = Field(default=None, max_length=5)  # Friday prayer (optional)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["SpiritualTask"] = Relationship(back_populates="masjid")


class SpiritualTask(SQLModel, table=True):
    """Spiritual task model for Islamic activities"""
    __tablename__ = "spiritual_tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=2000)
    category: TaskCategory = Field(default=TaskCategory.OTHER)
    priority: Priority = Field(default=Priority.MEDIUM, index=True)
    tags: Optional[str] = Field(default=None, max_length=500)  # Comma-separated

    # Masjid relationship
    masjid_id: Optional[int] = Field(default=None, foreign_key="masjids.id")
    masjid: Optional[Masjid] = Relationship(back_populates="tasks")

    # Scheduling
    due_datetime: Optional[datetime] = Field(default=None)
    recurrence: Recurrence = Field(default=Recurrence.NONE)

    # Status
    completed: bool = Field(default=False, index=True)
    completed_at: Optional[datetime] = Field(default=None)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class DailyHadith(SQLModel, table=True):
    """Daily hadith model for spiritual inspiration"""
    __tablename__ = "daily_hadith"

    id: Optional[int] = Field(default=None, primary_key=True)
    hadith_date: date = Field(index=True, unique=True)  # One hadith per day
    arabic_text: str = Field(max_length=2000)
    english_translation: str = Field(max_length=2000)
    narrator: str = Field(max_length=200)
    source: str = Field(max_length=200)  # e.g., "Sahih Bukhari 123"
    theme: Optional[str] = Field(default=None, max_length=100)  # e.g., "Patience", "Prayer"
    created_at: datetime = Field(default_factory=datetime.utcnow)
