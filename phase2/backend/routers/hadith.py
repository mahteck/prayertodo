"""
SalaatFlow Phase II - Daily Hadith Router

REST API endpoints for daily hadith management.
Provides endpoints to create, retrieve, and manage hadith of the day.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, col
from datetime import datetime, date

from database import get_session
from models import DailyHadith


# ============================================================================
# Router Configuration
# ============================================================================

router = APIRouter()


# ============================================================================
# Daily Hadith Endpoints
# ============================================================================

@router.get("/daily", response_model=DailyHadith)
async def get_daily_hadith(
    session: Session = Depends(get_session),
    date_param: Optional[str] = Query(None, description="Date in YYYY-MM-DD format (defaults to today)")
) -> DailyHadith:
    """
    Get the hadith for a specific date (defaults to today).

    Args:
        session: Database session
        date_param: Optional date string in YYYY-MM-DD format

    Returns:
        DailyHadith: Hadith for the specified date

    Raises:
        HTTPException: 404 if no hadith found for the date
    """
    # Parse date or use today
    if date_param:
        try:
            target_date = datetime.strptime(date_param, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD"
            )
    else:
        target_date = date.today()

    # Query for hadith on this date (match by date only, not time)
    hadith = session.exec(
        select(DailyHadith).where(
            col(DailyHadith.date).cast(date) == target_date
        )
    ).first()

    if not hadith:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No hadith found for date {target_date}"
        )

    return hadith


@router.post("/", response_model=DailyHadith, status_code=status.HTTP_201_CREATED)
async def create_hadith(
    hadith: DailyHadith,
    session: Session = Depends(get_session)
) -> DailyHadith:
    """
    Create a new daily hadith entry.

    Args:
        hadith: Hadith data
        session: Database session

    Returns:
        DailyHadith: Created hadith with assigned ID

    Raises:
        HTTPException: 400 if hadith already exists for this date
    """
    # Check for duplicate date
    hadith_date = hadith.date.date() if isinstance(hadith.date, datetime) else hadith.date

    existing = session.exec(
        select(DailyHadith).where(
            col(DailyHadith.date).cast(date) == hadith_date
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Hadith already exists for date {hadith_date}"
        )

    # Set timestamp
    hadith.created_at = datetime.utcnow()

    # Add to database
    session.add(hadith)
    session.commit()
    session.refresh(hadith)

    return hadith


@router.get("/{hadith_id}", response_model=DailyHadith)
async def get_hadith(
    hadith_id: int,
    session: Session = Depends(get_session)
) -> DailyHadith:
    """
    Get a specific hadith by ID.

    Args:
        hadith_id: Hadith ID
        session: Database session

    Returns:
        DailyHadith: Hadith details

    Raises:
        HTTPException: 404 if hadith not found
    """
    hadith = session.get(DailyHadith, hadith_id)
    if not hadith:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hadith with ID {hadith_id} not found"
        )
    return hadith


@router.get("/", response_model=List[DailyHadith])
async def list_hadith(
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    sort_order: str = Query("desc", description="Sort by date: asc or desc"),
) -> List[DailyHadith]:
    """
    List all hadith entries with pagination.

    Query Parameters:
        - skip: Number of records to skip (pagination)
        - limit: Maximum records to return (default: 100, max: 1000)
        - sort_order: Sort by date - asc or desc (default: desc)

    Returns:
        List[DailyHadith]: List of hadith entries
    """
    # Build query
    query = select(DailyHadith)

    # Apply sorting by date
    if sort_order.lower() == "asc":
        query = query.order_by(col(DailyHadith.date).asc())
    else:
        query = query.order_by(col(DailyHadith.date).desc())

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute query
    hadith_list = session.exec(query).all()
    return hadith_list


@router.put("/{hadith_id}", response_model=DailyHadith)
async def update_hadith(
    hadith_id: int,
    hadith_update: DailyHadith,
    session: Session = Depends(get_session)
) -> DailyHadith:
    """
    Update an existing hadith entry.

    Args:
        hadith_id: Hadith ID to update
        hadith_update: Updated hadith data
        session: Database session

    Returns:
        DailyHadith: Updated hadith

    Raises:
        HTTPException: 404 if hadith not found, 400 if date conflict
    """
    # Get existing hadith
    hadith = session.get(DailyHadith, hadith_id)
    if not hadith:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hadith with ID {hadith_id} not found"
        )

    # Check for date conflict (if date is being changed)
    if hadith_update.date:
        new_date = hadith_update.date.date() if isinstance(hadith_update.date, datetime) else hadith_update.date
        current_date = hadith.date.date() if isinstance(hadith.date, datetime) else hadith.date

        if new_date != current_date:
            existing = session.exec(
                select(DailyHadith).where(
                    col(DailyHadith.date).cast(date) == new_date
                )
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Hadith already exists for date {new_date}"
                )

    # Update fields (excluding ID and created_at)
    hadith_data = hadith_update.model_dump(exclude_unset=True, exclude={"id", "created_at"})
    for key, value in hadith_data.items():
        setattr(hadith, key, value)

    # Save to database
    session.add(hadith)
    session.commit()
    session.refresh(hadith)

    return hadith


@router.delete("/{hadith_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hadith(
    hadith_id: int,
    session: Session = Depends(get_session)
) -> None:
    """
    Delete a hadith entry.

    Args:
        hadith_id: Hadith ID to delete
        session: Database session

    Raises:
        HTTPException: 404 if hadith not found
    """
    hadith = session.get(DailyHadith, hadith_id)
    if not hadith:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hadith with ID {hadith_id} not found"
        )

    session.delete(hadith)
    session.commit()
