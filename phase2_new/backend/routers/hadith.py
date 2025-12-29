"""
Hadith router - Daily hadith management
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, date

from database import get_session
from models import DailyHadith


router = APIRouter()


# GET /hadith/today - Get today's hadith
@router.get("/today", response_model=DailyHadith)
async def get_todays_hadith(
    session: Session = Depends(get_session),
) -> DailyHadith:
    """
    Get the hadith for today's date
    """
    today = date.today()
    query = select(DailyHadith).where(DailyHadith.hadith_date == today)
    hadith = session.exec(query).first()

    if not hadith:
        raise HTTPException(
            status_code=404,
            detail=f"No hadith found for today ({today})"
        )

    return hadith


# GET /hadith - List all hadith
@router.get("/", response_model=List[DailyHadith])
async def list_hadith(
    session: Session = Depends(get_session),
    theme: Optional[str] = Query(None, description="Filter by theme"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
) -> List[DailyHadith]:
    """
    List all daily hadith entries
    """
    query = select(DailyHadith).order_by(DailyHadith.hadith_date.desc())

    if theme:
        query = query.where(DailyHadith.theme.ilike(f"%{theme}%"))

    query = query.offset(skip).limit(limit)

    hadith_list = session.exec(query).all()
    return hadith_list


# GET /hadith/date/{date} - Get hadith by specific date
@router.get("/date/{hadith_date}", response_model=DailyHadith)
async def get_hadith_by_date(
    hadith_date: date,
    session: Session = Depends(get_session),
) -> DailyHadith:
    """
    Get hadith for a specific date (format: YYYY-MM-DD)
    """
    query = select(DailyHadith).where(DailyHadith.hadith_date == hadith_date)
    hadith = session.exec(query).first()

    if not hadith:
        raise HTTPException(
            status_code=404,
            detail=f"No hadith found for date {hadith_date}"
        )

    return hadith


# GET /hadith/{id} - Get hadith by ID
@router.get("/{id}", response_model=DailyHadith)
async def get_hadith(
    id: int,
    session: Session = Depends(get_session),
) -> DailyHadith:
    """
    Get a hadith by ID
    """
    hadith = session.get(DailyHadith, id)
    if not hadith:
        raise HTTPException(status_code=404, detail=f"Hadith with id {id} not found")
    return hadith


# POST /hadith - Create new hadith entry
@router.post("/", response_model=DailyHadith, status_code=201)
async def create_hadith(
    hadith: DailyHadith,
    session: Session = Depends(get_session),
) -> DailyHadith:
    """
    Create a new daily hadith entry
    Note: hadith_date must be unique
    """
    # Check if hadith already exists for this date
    existing = session.exec(
        select(DailyHadith).where(DailyHadith.hadith_date == hadith.hadith_date)
    ).first()

    if existing:
        raise HTTPException(
            status_code=422,
            detail=f"Hadith already exists for date {hadith.hadith_date}"
        )

    hadith.created_at = datetime.utcnow()

    session.add(hadith)
    session.commit()
    session.refresh(hadith)
    return hadith


# PUT /hadith/{id} - Update hadith
@router.put("/{id}", response_model=DailyHadith)
async def update_hadith(
    id: int,
    updated_hadith: DailyHadith,
    session: Session = Depends(get_session),
) -> DailyHadith:
    """
    Update an existing hadith entry
    """
    hadith = session.get(DailyHadith, id)
    if not hadith:
        raise HTTPException(status_code=404, detail=f"Hadith with id {id} not found")

    # Check if new date conflicts with another hadith
    if updated_hadith.hadith_date != hadith.hadith_date:
        existing = session.exec(
            select(DailyHadith).where(DailyHadith.hadith_date == updated_hadith.hadith_date)
        ).first()
        if existing:
            raise HTTPException(
                status_code=422,
                detail=f"Hadith already exists for date {updated_hadith.hadith_date}"
            )

    hadith_data = updated_hadith.model_dump(exclude_unset=True, exclude={"id", "created_at"})
    for key, value in hadith_data.items():
        setattr(hadith, key, value)

    session.add(hadith)
    session.commit()
    session.refresh(hadith)
    return hadith


# DELETE /hadith/{id} - Delete hadith
@router.delete("/{id}", status_code=204)
async def delete_hadith(
    id: int,
    session: Session = Depends(get_session),
) -> None:
    """
    Delete a hadith entry
    """
    hadith = session.get(DailyHadith, id)
    if not hadith:
        raise HTTPException(status_code=404, detail=f"Hadith with id {id} not found")

    session.delete(hadith)
    session.commit()
