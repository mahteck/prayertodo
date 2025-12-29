"""
Tasks router - CRUD operations for spiritual tasks
Includes filtering, sorting, search, and bulk operations
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func, or_
from typing import List, Optional
from datetime import datetime, timedelta

from database import get_session
from models import SpiritualTask, TaskCategory, Priority, Recurrence, Masjid


router = APIRouter()


# GET /tasks - List all tasks with filtering, sorting, and pagination
@router.get("/", response_model=List[SpiritualTask])
async def list_tasks(
    session: Session = Depends(get_session),
    # Filters
    category: Optional[TaskCategory] = Query(None, description="Filter by category"),
    priority: Optional[Priority] = Query(None, description="Filter by priority"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    masjid_id: Optional[int] = Query(None, description="Filter by masjid"),
    recurrence: Optional[Recurrence] = Query(None, description="Filter by recurrence"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    # Sorting
    sort_by: Optional[str] = Query("created_at", description="Field to sort by"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    # Pagination
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
) -> List[SpiritualTask]:
    """
    List all spiritual tasks with optional filtering, sorting, and pagination
    """
    # Build query
    query = select(SpiritualTask)

    # Apply filters
    if category:
        query = query.where(SpiritualTask.category == category)

    if priority:
        query = query.where(SpiritualTask.priority == priority)

    if completed is not None:
        query = query.where(SpiritualTask.completed == completed)

    if masjid_id:
        query = query.where(SpiritualTask.masjid_id == masjid_id)

    if recurrence:
        query = query.where(SpiritualTask.recurrence == recurrence)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            or_(
                SpiritualTask.title.ilike(search_pattern),
                SpiritualTask.description.ilike(search_pattern),
            )
        )

    # Apply sorting
    if sort_order.lower() == "desc":
        query = query.order_by(getattr(SpiritualTask, sort_by).desc())
    else:
        query = query.order_by(getattr(SpiritualTask, sort_by))

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute query
    tasks = session.exec(query).all()
    return tasks


# GET /tasks/upcoming - Get upcoming tasks (within next N days)
@router.get("/upcoming", response_model=List[SpiritualTask])
async def get_upcoming_tasks(
    session: Session = Depends(get_session),
    days: int = Query(7, ge=1, le=30, description="Number of days to look ahead"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of tasks"),
) -> List[SpiritualTask]:
    """
    Get upcoming tasks with due dates within the next N days
    """
    now = datetime.utcnow()
    future = now + timedelta(days=days)

    query = (
        select(SpiritualTask)
        .where(SpiritualTask.completed == False)
        .where(SpiritualTask.due_datetime.isnot(None))
        .where(SpiritualTask.due_datetime >= now)
        .where(SpiritualTask.due_datetime <= future)
        .order_by(SpiritualTask.due_datetime)
        .limit(limit)
    )

    tasks = session.exec(query).all()
    return tasks


# GET /tasks/stats/summary - Get task statistics
@router.get("/stats/summary", response_model=dict)
async def get_task_statistics(session: Session = Depends(get_session)) -> dict:
    """
    Get comprehensive statistics about tasks
    """
    all_tasks = session.exec(select(SpiritualTask)).all()

    total = len(all_tasks)
    completed = sum(1 for t in all_tasks if t.completed)
    pending = total - completed
    completion_rate = (completed / total * 100) if total > 0 else 0

    # By category
    by_category = {}
    for cat in TaskCategory:
        cat_tasks = [t for t in all_tasks if t.category == cat]
        by_category[cat.value] = {
            "total": len(cat_tasks),
            "completed": sum(1 for t in cat_tasks if t.completed),
            "pending": sum(1 for t in cat_tasks if not t.completed),
        }

    # By priority
    by_priority = {}
    for pri in Priority:
        pri_tasks = [t for t in all_tasks if t.priority == pri]
        by_priority[pri.value] = {
            "total": len(pri_tasks),
            "completed": sum(1 for t in pri_tasks if t.completed),
            "pending": sum(1 for t in pri_tasks if not t.completed),
        }

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "completion_rate": round(completion_rate, 2),
        "by_category": by_category,
        "by_priority": by_priority,
    }


# GET /tasks/{id} - Get single task by ID
@router.get("/{id}", response_model=SpiritualTask)
async def get_task(
    id: int,
    session: Session = Depends(get_session),
) -> SpiritualTask:
    """
    Get a single task by ID
    """
    task = session.get(SpiritualTask, id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    return task


# POST /tasks - Create new task
@router.post("/", response_model=SpiritualTask, status_code=201)
async def create_task(
    task: SpiritualTask,
    session: Session = Depends(get_session),
) -> SpiritualTask:
    """
    Create a new spiritual task
    """
    # Validate masjid_id if provided
    if task.masjid_id:
        masjid = session.get(Masjid, task.masjid_id)
        if not masjid:
            raise HTTPException(
                status_code=422,
                detail=f"Masjid with id {task.masjid_id} not found"
            )

    # Set timestamps
    task.created_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# PUT /tasks/{id} - Update task
@router.put("/{id}", response_model=SpiritualTask)
async def update_task(
    id: int,
    updated_task: SpiritualTask,
    session: Session = Depends(get_session),
) -> SpiritualTask:
    """
    Update an existing task
    """
    task = session.get(SpiritualTask, id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")

    # Validate masjid_id if changed
    if updated_task.masjid_id and updated_task.masjid_id != task.masjid_id:
        masjid = session.get(Masjid, updated_task.masjid_id)
        if not masjid:
            raise HTTPException(
                status_code=422,
                detail=f"Masjid with id {updated_task.masjid_id} not found"
            )

    # Update fields
    task_data = updated_task.model_dump(exclude_unset=True, exclude={"id", "created_at"})
    for key, value in task_data.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# PATCH /tasks/{id}/complete - Mark task as complete
@router.patch("/{id}/complete", response_model=SpiritualTask)
async def complete_task(
    id: int,
    session: Session = Depends(get_session),
) -> SpiritualTask:
    """
    Mark a task as completed
    """
    task = session.get(SpiritualTask, id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")

    task.completed = True
    task.completed_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# PATCH /tasks/{id}/incomplete - Mark task as incomplete
@router.patch("/{id}/incomplete", response_model=SpiritualTask)
async def uncomplete_task(
    id: int,
    session: Session = Depends(get_session),
) -> SpiritualTask:
    """
    Mark a task as incomplete
    """
    task = session.get(SpiritualTask, id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")

    task.completed = False
    task.completed_at = None
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# DELETE /tasks/{id} - Delete task
@router.delete("/{id}", status_code=204)
async def delete_task(
    id: int,
    session: Session = Depends(get_session),
) -> None:
    """
    Delete a task by ID
    """
    task = session.get(SpiritualTask, id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")

    session.delete(task)
    session.commit()


# POST /tasks/bulk/complete - Mark multiple tasks as complete
@router.post("/bulk/complete", response_model=dict)
async def bulk_complete_tasks(
    task_ids: List[int],
    session: Session = Depends(get_session),
) -> dict:
    """
    Mark multiple tasks as completed
    """
    updated = 0
    not_found = []

    for task_id in task_ids:
        task = session.get(SpiritualTask, task_id)
        if task:
            task.completed = True
            task.completed_at = datetime.utcnow()
            task.updated_at = datetime.utcnow()
            session.add(task)
            updated += 1
        else:
            not_found.append(task_id)

    session.commit()

    return {
        "updated": updated,
        "not_found": not_found,
        "message": f"Successfully marked {updated} tasks as complete",
    }


# DELETE /tasks/bulk/delete - Delete multiple tasks
@router.post("/bulk/delete", response_model=dict)
async def bulk_delete_tasks(
    task_ids: List[int],
    session: Session = Depends(get_session),
) -> dict:
    """
    Delete multiple tasks
    """
    deleted = 0
    not_found = []

    for task_id in task_ids:
        task = session.get(SpiritualTask, task_id)
        if task:
            session.delete(task)
            deleted += 1
        else:
            not_found.append(task_id)

    session.commit()

    return {
        "deleted": deleted,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted} tasks",
    }
