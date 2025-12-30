"""
Database Client for MCP Tools
Direct database access to avoid circular HTTP dependencies

This module provides direct database access for MCP tools,
eliminating the need for HTTP calls to the same server.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlmodel import Session

from database import engine
from models import SpiritualTask, Masjid, DailyHadith
from chatbot.mcp_tools.base import ToolResult

logger = logging.getLogger(__name__)


class DatabaseClient:
    """Direct database client for MCP tools"""

    @staticmethod
    def create_task(
        user_id: int,
        title: str,
        category: str = "Other",
        priority: str = "medium",
        description: Optional[str] = None,
        due_datetime: Optional[str] = None,
        masjid_id: Optional[int] = None,
        linked_prayer: Optional[str] = None,
        recurrence: Optional[str] = None,
        recurrence_pattern: Optional[str] = None,
        minutes_before_prayer: Optional[int] = None,
        **kwargs
    ) -> ToolResult:
        """Create a new spiritual task"""
        try:
            with Session(engine) as session:
                # Create task (uppercase enum values for database)
                task = SpiritualTask(
                    user_id=user_id,
                    title=title,
                    description=description or "",
                    category=category.upper() if category else "OTHER",
                    priority=priority.upper() if priority else "MEDIUM",
                    masjid_id=masjid_id,
                    linked_prayer=linked_prayer.upper() if linked_prayer else None,
                    recurrence=recurrence.upper() if recurrence else "NONE",
                    recurrence_pattern=recurrence_pattern,
                    minutes_before_prayer=minutes_before_prayer,
                    completed=False
                )

                # Parse due_datetime if provided
                if due_datetime:
                    try:
                        task.due_datetime = datetime.fromisoformat(due_datetime.replace('Z', '+00:00'))
                    except (ValueError, AttributeError):
                        pass

                session.add(task)
                session.commit()
                session.refresh(task)

                return ToolResult(
                    success=True,
                    data={
                        "task_id": task.id,
                        "title": task.title,
                        "category": task.category,
                        "priority": task.priority,
                        "completed": task.completed
                    }
                )
        except Exception as e:
            logger.error(f"Failed to create task: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="DATABASE_ERROR",
                error_message=f"Failed to create task: {str(e)}"
            )

    @staticmethod
    def list_tasks(
        user_id: int,
        category: Optional[str] = None,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        **kwargs
    ) -> ToolResult:
        """List user's tasks with optional filters"""
        try:
            with Session(engine) as session:
                query = session.query(SpiritualTask).filter(
                    SpiritualTask.user_id == user_id
                )

                if category:
                    query = query.filter(SpiritualTask.category == category)
                if completed is not None:
                    query = query.filter(SpiritualTask.completed == completed)
                if priority:
                    query = query.filter(SpiritualTask.priority == priority)

                tasks = query.order_by(SpiritualTask.created_at.desc()).all()

                return ToolResult(
                    success=True,
                    data={
                        "tasks": [
                            {
                                "id": task.id,
                                "title": task.title,
                                "category": task.category,
                                "priority": task.priority,
                                "completed": task.completed,
                                "linked_prayer": task.linked_prayer,
                                "created_at": task.created_at.isoformat() if task.created_at else None
                            }
                            for task in tasks
                        ],
                        "total": len(tasks)
                    }
                )
        except Exception as e:
            logger.error(f"Failed to list tasks: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="DATABASE_ERROR",
                error_message=f"Failed to list tasks: {str(e)}"
            )

    @staticmethod
    def update_task(
        user_id: int,
        task_id: int,
        **kwargs
    ) -> ToolResult:
        """Update an existing task"""
        try:
            with Session(engine) as session:
                task = session.query(SpiritualTask).filter(
                    SpiritualTask.id == task_id,
                    SpiritualTask.user_id == user_id
                ).first()

                if not task:
                    return ToolResult(
                        success=False,
                        error="NOT_FOUND",
                        error_message=f"Task {task_id} not found"
                    )

                # Update fields
                for key, value in kwargs.items():
                    if hasattr(task, key) and value is not None:
                        setattr(task, key, value)

                session.commit()
                session.refresh(task)

                return ToolResult(
                    success=True,
                    data={"task_id": task.id, "title": task.title}
                )
        except Exception as e:
            logger.error(f"Failed to update task: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="DATABASE_ERROR",
                error_message=f"Failed to update task: {str(e)}"
            )

    @staticmethod
    def delete_task(user_id: int, task_id: int, **kwargs) -> ToolResult:
        """Delete a task"""
        try:
            with Session(engine) as session:
                task = session.query(SpiritualTask).filter(
                    SpiritualTask.id == task_id,
                    SpiritualTask.user_id == user_id
                ).first()

                if not task:
                    return ToolResult(
                        success=False,
                        error="NOT_FOUND",
                        error_message=f"Task {task_id} not found"
                    )

                session.delete(task)
                session.commit()

                return ToolResult(
                    success=True,
                    data={"message": "Task deleted successfully"}
                )
        except Exception as e:
            logger.error(f"Failed to delete task: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="DATABASE_ERROR",
                error_message=f"Failed to delete task: {str(e)}"
            )

    @staticmethod
    def complete_task(user_id: int, task_id: int, **kwargs) -> ToolResult:
        """Mark a task as completed"""
        try:
            with Session(engine) as session:
                task = session.query(SpiritualTask).filter(
                    SpiritualTask.id == task_id,
                    SpiritualTask.user_id == user_id
                ).first()

                if not task:
                    return ToolResult(
                        success=False,
                        error="NOT_FOUND",
                        error_message=f"Task {task_id} not found"
                    )

                task.completed = True
                session.commit()

                return ToolResult(
                    success=True,
                    data={"task_id": task.id, "completed": True}
                )
        except Exception as e:
            logger.error(f"Failed to complete task: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="DATABASE_ERROR",
                error_message=f"Failed to complete task: {str(e)}"
            )

    @staticmethod
    def list_masjids(area: Optional[str] = None, city: Optional[str] = None, **kwargs) -> ToolResult:
        """List masjids with optional filters"""
        try:
            with Session(engine) as session:
                query = session.query(Masjid)

                if area:
                    query = query.filter(Masjid.area_name.ilike(f"%{area}%"))
                if city:
                    query = query.filter(Masjid.city.ilike(f"%{city}%"))

                masjids = query.all()

                return ToolResult(
                    success=True,
                    data={
                        "masjids": [
                            {
                                "id": m.id,
                                "name": m.name,
                                "area_name": m.area_name,
                                "city": m.city,
                                "fajr_time": str(m.fajr_time) if m.fajr_time else None,
                                "dhuhr_time": str(m.dhuhr_time) if m.dhuhr_time else None
                            }
                            for m in masjids
                        ],
                        "total": len(masjids)
                    }
                )
        except Exception as e:
            logger.error(f"Failed to list masjids: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="DATABASE_ERROR",
                error_message=f"Failed to list masjids: {str(e)}"
            )

    @staticmethod
    def get_masjid_details(masjid_id: int, **kwargs) -> ToolResult:
        """Get detailed masjid information"""
        try:
            with Session(engine) as session:
                masjid = session.query(Masjid).filter(Masjid.id == masjid_id).first()

                if not masjid:
                    return ToolResult(
                        success=False,
                        error="NOT_FOUND",
                        error_message=f"Masjid {masjid_id} not found"
                    )

                return ToolResult(
                    success=True,
                    data={
                        "id": masjid.id,
                        "name": masjid.name,
                        "area_name": masjid.area_name,
                        "city": masjid.city,
                        "address": masjid.address,
                        "fajr_time": str(masjid.fajr_time) if masjid.fajr_time else None,
                        "dhuhr_time": str(masjid.dhuhr_time) if masjid.dhuhr_time else None,
                        "asr_time": str(masjid.asr_time) if masjid.asr_time else None,
                        "maghrib_time": str(masjid.maghrib_time) if masjid.maghrib_time else None,
                        "isha_time": str(masjid.isha_time) if masjid.isha_time else None,
                        "jummah_time": str(masjid.jummah_time) if masjid.jummah_time else None
                    }
                )
        except Exception as e:
            logger.error(f"Failed to get masjid details: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="DATABASE_ERROR",
                error_message=f"Failed to get masjid details: {str(e)}"
            )

    @staticmethod
    def search_masjids(
        name: Optional[str] = None,
        area: Optional[str] = None,
        city: Optional[str] = None,
        **kwargs
    ) -> ToolResult:
        """Search masjids by name, area, or city"""
        try:
            with Session(engine) as session:
                query = session.query(Masjid)

                if name:
                    query = query.filter(Masjid.name.ilike(f"%{name}%"))
                if area:
                    query = query.filter(Masjid.area_name.ilike(f"%{area}%"))
                if city:
                    query = query.filter(Masjid.city.ilike(f"%{city}%"))

                masjids = query.all()

                return ToolResult(
                    success=True,
                    data={
                        "masjids": [
                            {
                                "id": m.id,
                                "name": m.name,
                                "area_name": m.area_name,
                                "city": m.city,
                                "address": m.address
                            }
                            for m in masjids
                        ],
                        "total": len(masjids)
                    }
                )
        except Exception as e:
            logger.error(f"Failed to search masjids: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="DATABASE_ERROR",
                error_message=f"Failed to search masjids: {str(e)}"
            )

    @staticmethod
    def get_current_prayer(masjid_id: int, **kwargs) -> ToolResult:
        """Get current or next upcoming prayer for a masjid"""
        try:
            with Session(engine) as session:
                masjid = session.query(Masjid).filter(Masjid.id == masjid_id).first()

                if not masjid:
                    return ToolResult(
                        success=False,
                        error="NOT_FOUND",
                        error_message=f"Masjid {masjid_id} not found"
                    )

                # Get current time
                from datetime import datetime, time
                now = datetime.now().time()

                # Find next prayer
                prayers = [
                    ("Fajr", masjid.fajr_time),
                    ("Dhuhr", masjid.dhuhr_time),
                    ("Asr", masjid.asr_time),
                    ("Maghrib", masjid.maghrib_time),
                    ("Isha", masjid.isha_time),
                ]

                next_prayer = None
                for prayer_name, prayer_time in prayers:
                    if prayer_time and prayer_time > now:
                        next_prayer = (prayer_name, prayer_time)
                        break

                # If no prayer found after current time, wrap to Fajr
                if not next_prayer and masjid.fajr_time:
                    next_prayer = ("Fajr", masjid.fajr_time)

                if next_prayer:
                    return ToolResult(
                        success=True,
                        data={
                            "masjid_id": masjid.id,
                            "masjid_name": masjid.name,
                            "current_prayer": next_prayer[0],
                            "prayer_time": str(next_prayer[1])
                        }
                    )
                else:
                    return ToolResult(
                        success=False,
                        error="NOT_FOUND",
                        error_message="No prayer times available"
                    )
        except Exception as e:
            logger.error(f"Failed to get current prayer: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="DATABASE_ERROR",
                error_message=f"Failed to get current prayer: {str(e)}"
            )

    @staticmethod
    def get_daily_hadith(**kwargs) -> ToolResult:
        """Get today's hadith"""
        try:
            with Session(engine) as session:
                hadith = session.query(DailyHadith).order_by(
                    DailyHadith.created_at.desc()
                ).first()

                if not hadith:
                    return ToolResult(
                        success=False,
                        error="NOT_FOUND",
                        error_message="No hadith available"
                    )

                return ToolResult(
                    success=True,
                    data={
                        "hadith_text_en": hadith.hadith_text_en,
                        "hadith_text_ur": hadith.hadith_text_ur,
                        "source": hadith.source,
                        "date": hadith.created_at.isoformat() if hadith.created_at else None
                    }
                )
        except Exception as e:
            logger.error(f"Failed to get daily hadith: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="DATABASE_ERROR",
                error_message=f"Failed to get daily hadith: {str(e)}"
            )

    @staticmethod
    def get_random_hadith(**kwargs) -> ToolResult:
        """Get a random hadith"""
        try:
            with Session(engine) as session:
                from sqlalchemy import func
                hadith = session.query(DailyHadith).order_by(func.random()).first()

                if not hadith:
                    return ToolResult(
                        success=False,
                        error="NOT_FOUND",
                        error_message="No hadith available"
                    )

                return ToolResult(
                    success=True,
                    data={
                        "hadith_text_en": hadith.hadith_text_en,
                        "hadith_text_ur": hadith.hadith_text_ur,
                        "source": hadith.source,
                        "date": hadith.created_at.isoformat() if hadith.created_at else None
                    }
                )
        except Exception as e:
            logger.error(f"Failed to get random hadith: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="DATABASE_ERROR",
                error_message=f"Failed to get random hadith: {str(e)}"
            )


# Singleton instance
_db_client = DatabaseClient()

def get_db_client() -> DatabaseClient:
    """Get the database client instance"""
    return _db_client
