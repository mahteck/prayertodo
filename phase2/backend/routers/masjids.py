"""
SalaatFlow Phase II - Masjid Router

REST API endpoints for masjid (mosque) management.
Provides CRUD operations and task association queries.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, col
from datetime import datetime

from database import get_session
from models import Masjid, SpiritualTask


# ============================================================================
# Router Configuration
# ============================================================================

router = APIRouter()


# ============================================================================
# CRUD Endpoints
# ============================================================================

@router.post("/", response_model=Masjid, status_code=status.HTTP_201_CREATED)
async def create_masjid(
    masjid: Masjid,
    session: Session = Depends(get_session)
) -> Masjid:
    """
    Create a new masjid.

    Args:
        masjid: Masjid data (without ID)
        session: Database session

    Returns:
        Masjid: Created masjid with assigned ID

    Raises:
        HTTPException: 400 if masjid name already exists
    """
    # Check for duplicate name
    existing = session.exec(
        select(Masjid).where(Masjid.name == masjid.name)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Masjid with name '{masjid.name}' already exists"
        )

    # Set timestamps
    masjid.created_at = datetime.utcnow()
    masjid.updated_at = datetime.utcnow()

    # Add to database
    session.add(masjid)
    session.commit()
    session.refresh(masjid)

    return masjid


@router.get("/", response_model=List[Masjid])
async def list_masjids(
    session: Session = Depends(get_session),
    # Filtering parameters
    area: Optional[str] = Query(None, description="Filter by area"),
    city: Optional[str] = Query(None, description="Filter by city"),
    # Sorting parameters
    sort_by: Optional[str] = Query("name", description="Field to sort by"),
    sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    # Pagination
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
) -> List[Masjid]:
    """
    List all masjids with optional filtering, sorting, and pagination.

    Query Parameters:
        - area: Filter by area (exact match)
        - city: Filter by city (exact match)
        - sort_by: Field to sort by (default: name)
        - sort_order: Sort order - asc or desc (default: asc)
        - skip: Number of records to skip (pagination)
        - limit: Maximum records to return (default: 100, max: 1000)

    Returns:
        List[Masjid]: List of masjids matching criteria
    """
    # Build query
    query = select(Masjid)

    # Apply filters
    if area:
        query = query.where(Masjid.area == area)
    if city:
        query = query.where(Masjid.city == city)

    # Apply sorting
    sort_field = getattr(Masjid, sort_by, Masjid.name)
    if sort_order.lower() == "desc":
        query = query.order_by(col(sort_field).desc())
    else:
        query = query.order_by(col(sort_field).asc())

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute query
    masjids = session.exec(query).all()
    return masjids


@router.get("/{masjid_id}", response_model=Masjid)
async def get_masjid(
    masjid_id: int,
    session: Session = Depends(get_session)
) -> Masjid:
    """
    Get a specific masjid by ID.

    Args:
        masjid_id: Masjid ID
        session: Database session

    Returns:
        Masjid: Masjid details

    Raises:
        HTTPException: 404 if masjid not found
    """
    masjid = session.get(Masjid, masjid_id)
    if not masjid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Masjid with ID {masjid_id} not found"
        )
    return masjid


@router.put("/{masjid_id}", response_model=Masjid)
async def update_masjid(
    masjid_id: int,
    masjid_update: Masjid,
    session: Session = Depends(get_session)
) -> Masjid:
    """
    Update an existing masjid.

    Args:
        masjid_id: Masjid ID to update
        masjid_update: Updated masjid data
        session: Database session

    Returns:
        Masjid: Updated masjid

    Raises:
        HTTPException: 404 if masjid not found, 400 if name conflict
    """
    # Get existing masjid
    masjid = session.get(Masjid, masjid_id)
    if not masjid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Masjid with ID {masjid_id} not found"
        )

    # Check for name conflict (if name is being changed)
    if masjid_update.name and masjid_update.name != masjid.name:
        existing = session.exec(
            select(Masjid).where(Masjid.name == masjid_update.name)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Masjid with name '{masjid_update.name}' already exists"
            )

    # Update fields (excluding ID and created_at)
    masjid_data = masjid_update.model_dump(exclude_unset=True, exclude={"id", "created_at"})
    for key, value in masjid_data.items():
        setattr(masjid, key, value)

    # Update timestamp
    masjid.updated_at = datetime.utcnow()

    # Save to database
    session.add(masjid)
    session.commit()
    session.refresh(masjid)

    return masjid


@router.delete("/{masjid_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_masjid(
    masjid_id: int,
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a masjid.

    Note: This will set masjid_id to NULL for all associated tasks.

    Args:
        masjid_id: Masjid ID to delete
        session: Database session

    Raises:
        HTTPException: 404 if masjid not found
    """
    masjid = session.get(Masjid, masjid_id)
    if not masjid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Masjid with ID {masjid_id} not found"
        )

    # Nullify masjid_id in associated tasks
    tasks = session.exec(
        select(SpiritualTask).where(SpiritualTask.masjid_id == masjid_id)
    ).all()

    for task in tasks:
        task.masjid_id = None
        task.updated_at = datetime.utcnow()
        session.add(task)

    # Delete masjid
    session.delete(masjid)
    session.commit()


# ============================================================================
# Task Association Endpoints
# ============================================================================

@router.get("/{masjid_id}/tasks", response_model=List[SpiritualTask])
async def get_masjid_tasks(
    masjid_id: int,
    session: Session = Depends(get_session),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> List[SpiritualTask]:
    """
    Get all tasks associated with a specific masjid.

    Args:
        masjid_id: Masjid ID
        session: Database session
        completed: Optional filter by completion status
        skip: Records to skip (pagination)
        limit: Maximum records to return

    Returns:
        List[SpiritualTask]: Tasks associated with the masjid

    Raises:
        HTTPException: 404 if masjid not found
    """
    # Verify masjid exists
    masjid = session.get(Masjid, masjid_id)
    if not masjid:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Masjid with ID {masjid_id} not found"
        )

    # Build query
    query = select(SpiritualTask).where(SpiritualTask.masjid_id == masjid_id)

    # Apply completion filter if provided
    if completed is not None:
        query = query.where(SpiritualTask.completed == completed)

    # Apply pagination and ordering
    query = query.order_by(col(SpiritualTask.created_at).desc()).offset(skip).limit(limit)

    # Execute query
    tasks = session.exec(query).all()
    return tasks


# ============================================================================
# Search Endpoint
# ============================================================================

@router.get("/search/query", response_model=List[Masjid])
async def search_masjids(
    q: str = Query(..., min_length=1, description="Search query string"),
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
) -> List[Masjid]:
    """
    Search masjids by name or area (case-insensitive).

    Args:
        q: Search query string
        session: Database session
        skip: Records to skip (pagination)
        limit: Maximum records to return

    Returns:
        List[Masjid]: Matching masjids
    """
    # Build search query (case-insensitive partial match)
    from sqlmodel import or_

    search_pattern = f"%{q}%"
    query = select(Masjid).where(
        or_(
            Masjid.name.ilike(search_pattern),
            Masjid.area.ilike(search_pattern)
        )
    ).offset(skip).limit(limit)

    masjids = session.exec(query).all()
    return masjids
