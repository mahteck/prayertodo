"""
SalaatFlow Phase II - Task Router

REST API endpoints for spiritual task management.
Provides CRUD operations, filtering, sorting, and search functionality.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, or_, and_, col
from datetime import datetime

from database import get_session
from models import SpiritualTask, TaskCategory, Priority, Recurrence


# ============================================================================
# Router Configuration
# ============================================================================

router = APIRouter()


# ============================================================================
# CRUD Endpoints
# ============================================================================

@router.post("/", response_model=SpiritualTask, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: SpiritualTask,
    session: Session = Depends(get_session)
) -> SpiritualTask:
    """
    Create a new spiritual task.

    Args:
        task: Task data (without ID)
        session: Database session

    Returns:
        SpiritualTask: Created task with assigned ID

    Raises:
        HTTPException: 400 if validation fails
    """
    # Set timestamps
    task.created_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()

    # Add to database
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/", response_model=List[SpiritualTask])
async def list_tasks(
    session: Session = Depends(get_session),
    # Filtering parameters
    category: Optional[TaskCategory] = Query(None, description="Filter by category"),
    priority: Optional[Priority] = Query(None, description="Filter by priority"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    masjid_id: Optional[int] = Query(None, description="Filter by masjid ID"),
    recurrence: Optional[Recurrence] = Query(None, description="Filter by recurrence type"),
    # Sorting parameters
    sort_by: Optional[str] = Query("created_at", description="Field to sort by"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    # Pagination
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
) -> List[SpiritualTask]:
    """
    List all spiritual tasks with optional filtering, sorting, and pagination.

    Query Parameters:
        - category: Filter by task category (Farz, Sunnah, Nafl, Deed, Other)
        - priority: Filter by priority (Low, Medium, High, Urgent)
        - completed: Filter by completion status (true/false)
        - masjid_id: Filter by associated masjid
        - recurrence: Filter by recurrence type (None, Daily, Weekly, Monthly)
        - sort_by: Field to sort by (default: created_at)
        - sort_order: Sort order - asc or desc (default: desc)
        - skip: Number of records to skip (pagination)
        - limit: Maximum records to return (default: 100, max: 1000)

    Returns:
        List[SpiritualTask]: List of tasks matching criteria
    """
    # Build query
    query = select(SpiritualTask)

    # Apply filters
    filters = []
    if category is not None:
        filters.append(SpiritualTask.category == category)
    if priority is not None:
        filters.append(SpiritualTask.priority == priority)
    if completed is not None:
        filters.append(SpiritualTask.completed == completed)
    if masjid_id is not None:
        filters.append(SpiritualTask.masjid_id == masjid_id)
    if recurrence is not None:
        filters.append(SpiritualTask.recurrence == recurrence)

    if filters:
        query = query.where(and_(*filters))

    # Apply sorting
    sort_field = getattr(SpiritualTask, sort_by, SpiritualTask.created_at)
    if sort_order.lower() == "desc":
        query = query.order_by(col(sort_field).desc())
    else:
        query = query.order_by(col(sort_field).asc())

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute query
    tasks = session.exec(query).all()
    return tasks


@router.get("/{task_id}", response_model=SpiritualTask)
async def get_task(
    task_id: int,
    session: Session = Depends(get_session)
) -> SpiritualTask:
    """
    Get a specific spiritual task by ID.

    Args:
        task_id: Task ID
        session: Database session

    Returns:
        SpiritualTask: Task details

    Raises:
        HTTPException: 404 if task not found
    """
    task = session.get(SpiritualTask, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task


@router.put("/{task_id}", response_model=SpiritualTask)
async def update_task(
    task_id: int,
    task_update: SpiritualTask,
    session: Session = Depends(get_session)
) -> SpiritualTask:
    """
    Update an existing spiritual task.

    Args:
        task_id: Task ID to update
        task_update: Updated task data
        session: Database session

    Returns:
        SpiritualTask: Updated task

    Raises:
        HTTPException: 404 if task not found
    """
    # Get existing task
    task = session.get(SpiritualTask, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    # Update fields (excluding ID and created_at)
    task_data = task_update.model_dump(exclude_unset=True, exclude={"id", "created_at"})
    for key, value in task_data.items():
        setattr(task, key, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    # Save to database
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a spiritual task.

    Args:
        task_id: Task ID to delete
        session: Database session

    Raises:
        HTTPException: 404 if task not found
    """
    task = session.get(SpiritualTask, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    session.delete(task)
    session.commit()


# ============================================================================
# Task Completion Endpoints
# ============================================================================

@router.patch("/{task_id}/complete", response_model=SpiritualTask)
async def mark_task_complete(
    task_id: int,
    session: Session = Depends(get_session)
) -> SpiritualTask:
    """
    Mark a task as completed.

    Args:
        task_id: Task ID
        session: Database session

    Returns:
        SpiritualTask: Updated task

    Raises:
        HTTPException: 404 if task not found
    """
    task = session.get(SpiritualTask, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    task.completed = True
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.patch("/{task_id}/uncomplete", response_model=SpiritualTask)
async def mark_task_incomplete(
    task_id: int,
    session: Session = Depends(get_session)
) -> SpiritualTask:
    """
    Mark a task as incomplete (undo completion).

    Args:
        task_id: Task ID
        session: Database session

    Returns:
        SpiritualTask: Updated task

    Raises:
        HTTPException: 404 if task not found
    """
    task = session.get(SpiritualTask, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    task.completed = False
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


# ============================================================================
# Bulk Operations Endpoint
# ============================================================================

@router.post("/bulk/complete", response_model=dict)
async def bulk_complete_tasks(
    task_ids: List[int],
    session: Session = Depends(get_session)
) -> dict:
    """
    Mark multiple tasks as completed in a single operation.

    Args:
        task_ids: List of task IDs to mark as complete
        session: Database session

    Returns:
        dict: Summary of operation (updated count, failed IDs)
    """
    updated_count = 0
    failed_ids = []

    for task_id in task_ids:
        task = session.get(SpiritualTask, task_id)
        if task:
            task.completed = True
            task.updated_at = datetime.utcnow()
            session.add(task)
            updated_count += 1
        else:
            failed_ids.append(task_id)

    session.commit()

    return {
        "updated_count": updated_count,
        "failed_ids": failed_ids,
        "total_requested": len(task_ids)
    }


@router.delete("/bulk/delete", response_model=dict)
async def bulk_delete_tasks(
    task_ids: List[int],
    session: Session = Depends(get_session)
) -> dict:
    """
    Delete multiple tasks in a single operation.

    Args:
        task_ids: List of task IDs to delete
        session: Database session

    Returns:
        dict: Summary of operation (deleted count, failed IDs)
    """
    deleted_count = 0
    failed_ids = []

    for task_id in task_ids:
        task = session.get(SpiritualTask, task_id)
        if task:
            session.delete(task)
            deleted_count += 1
        else:
            failed_ids.append(task_id)

    session.commit()

    return {
        "deleted_count": deleted_count,
        "failed_ids": failed_ids,
        "total_requested": len(task_ids)
    }


# ============================================================================
# Search Endpoint
# ============================================================================

@router.get("/search/query", response_model=List[SpiritualTask])
async def search_tasks(
    q: str = Query(..., min_length=1, description="Search query string"),
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
) -> List[SpiritualTask]:
    """
    Search tasks by title or description (case-insensitive).

    Args:
        q: Search query string
        session: Database session
        skip: Records to skip (pagination)
        limit: Maximum records to return

    Returns:
        List[SpiritualTask]: Matching tasks
    """
    # Build search query (case-insensitive partial match)
    search_pattern = f"%{q}%"
    query = select(SpiritualTask).where(
        or_(
            SpiritualTask.title.ilike(search_pattern),
            SpiritualTask.description.ilike(search_pattern)
        )
    ).offset(skip).limit(limit)

    tasks = session.exec(query).all()
    return tasks


# ============================================================================
# Advanced Query Endpoints
# ============================================================================

@router.get("/stats/summary", response_model=dict)
async def get_task_statistics(
    session: Session = Depends(get_session)
) -> dict:
    """
    Get summary statistics about tasks.

    Returns:
        dict: Statistics including total, completed, pending counts by category
    """
    all_tasks = session.exec(select(SpiritualTask)).all()

    total = len(all_tasks)
    completed = sum(1 for t in all_tasks if t.completed)
    pending = total - completed

    # Group by category
    by_category = {}
    for category in TaskCategory:
        category_tasks = [t for t in all_tasks if t.category == category]
        by_category[category.value] = {
            "total": len(category_tasks),
            "completed": sum(1 for t in category_tasks if t.completed),
            "pending": len(category_tasks) - sum(1 for t in category_tasks if t.completed)
        }

    # Group by priority
    by_priority = {}
    for priority in Priority:
        priority_tasks = [t for t in all_tasks if t.priority == priority]
        by_priority[priority.value] = {
            "total": len(priority_tasks),
            "completed": sum(1 for t in priority_tasks if t.completed),
            "pending": len(priority_tasks) - sum(1 for t in priority_tasks if t.completed)
        }

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": round((completed / total * 100) if total > 0 else 0, 2),
        "by_category": by_category,
        "by_priority": by_priority
    }


@router.get("/upcoming", response_model=List[SpiritualTask])
async def get_upcoming_tasks(
    session: Session = Depends(get_session),
    days: int = Query(7, ge=1, le=30, description="Number of days to look ahead"),
    limit: int = Query(50, ge=1, le=500, description="Maximum tasks to return"),
) -> List[SpiritualTask]:
    """
    Get upcoming tasks due within the specified number of days.

    Args:
        session: Database session
        days: Number of days to look ahead (default: 7, max: 30)
        limit: Maximum tasks to return

    Returns:
        List[SpiritualTask]: Upcoming incomplete tasks sorted by due date
    """
    from datetime import timedelta

    now = datetime.utcnow()
    future_date = now + timedelta(days=days)

    query = select(SpiritualTask).where(
        and_(
            SpiritualTask.completed == False,
            SpiritualTask.due_datetime.isnot(None),
            SpiritualTask.due_datetime <= future_date,
            SpiritualTask.due_datetime >= now
        )
    ).order_by(SpiritualTask.due_datetime.asc()).limit(limit)

    tasks = session.exec(query).all()
    return tasks


@router.get("/overdue", response_model=List[SpiritualTask])
async def get_overdue_tasks(
    session: Session = Depends(get_session),
    limit: int = Query(50, ge=1, le=500, description="Maximum tasks to return"),
) -> List[SpiritualTask]:
    """
    Get overdue incomplete tasks.

    Args:
        session: Database session
        limit: Maximum tasks to return

    Returns:
        List[SpiritualTask]: Overdue tasks sorted by due date (oldest first)
    """
    now = datetime.utcnow()

    query = select(SpiritualTask).where(
        and_(
            SpiritualTask.completed == False,
            SpiritualTask.due_datetime.isnot(None),
            SpiritualTask.due_datetime < now
        )
    ).order_by(SpiritualTask.due_datetime.asc()).limit(limit)

    tasks = session.exec(query).all()
    return tasks
