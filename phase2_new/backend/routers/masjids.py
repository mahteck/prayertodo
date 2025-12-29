"""
Masjids router - CRUD operations for masjids (mosques)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func, col
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, validator
import re

from database import get_session
from models import Masjid, SpiritualTask


router = APIRouter()


# Pydantic schemas for request/response
class MasjidCreate(BaseModel):
    """Schema for creating a new masjid"""
    name: str
    area_name: str
    city: Optional[str] = None
    address: Optional[str] = None
    imam_name: Optional[str] = None
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fajr_time: str
    dhuhr_time: str
    asr_time: str
    maghrib_time: str
    isha_time: str
    jummah_time: Optional[str] = None

    @validator('fajr_time', 'dhuhr_time', 'asr_time', 'maghrib_time', 'isha_time', 'jummah_time')
    def validate_time_format(cls, v):
        if v is None:
            return v
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', v):
            raise ValueError('Time must be in HH:MM format (e.g., "05:30")')
        return v


class MasjidUpdate(BaseModel):
    """Schema for updating a masjid (all fields optional)"""
    name: Optional[str] = None
    area_name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    imam_name: Optional[str] = None
    phone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fajr_time: Optional[str] = None
    dhuhr_time: Optional[str] = None
    asr_time: Optional[str] = None
    maghrib_time: Optional[str] = None
    isha_time: Optional[str] = None
    jummah_time: Optional[str] = None

    @validator('fajr_time', 'dhuhr_time', 'asr_time', 'maghrib_time', 'isha_time', 'jummah_time')
    def validate_time_format(cls, v):
        if v is None:
            return v
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', v):
            raise ValueError('Time must be in HH:MM format (e.g., "05:30")')
        return v


# GET /masjids - List all masjids
@router.get("/")
async def list_masjids(
    session: Session = Depends(get_session),
    area_name: Optional[str] = Query(None, description="Filter by area name"),
    search: Optional[str] = Query(None, description="Search in name or area"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """
    List all masjids with optional filtering and pagination
    """
    query = select(Masjid)

    if area_name:
        query = query.where(col(Masjid.area_name) == area_name)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (col(Masjid.name).ilike(search_pattern)) |
            (col(Masjid.area_name).ilike(search_pattern))
        )

    # Count total
    count_query = select(func.count()).select_from(Masjid)
    if area_name:
        count_query = count_query.where(col(Masjid.area_name) == area_name)
    if search:
        count_query = count_query.where(
            (col(Masjid.name).ilike(search_pattern)) |
            (col(Masjid.area_name).ilike(search_pattern))
        )
    total = session.exec(count_query).one()

    # Paginate
    query = query.offset(offset).limit(limit)
    masjids = session.exec(query).all()

    return {
        "masjids": masjids,
        "total": total,
        "limit": limit,
        "offset": offset
    }


# GET /masjids/{id} - Get single masjid
@router.get("/{id}", response_model=Masjid)
async def get_masjid(
    id: int,
    session: Session = Depends(get_session),
) -> Masjid:
    """
    Get a single masjid by ID
    """
    masjid = session.get(Masjid, id)
    if not masjid:
        raise HTTPException(status_code=404, detail=f"Masjid with id {id} not found")
    return masjid


# GET /masjids/{id}/tasks - Get all tasks for a masjid
@router.get("/{id}/tasks", response_model=List[SpiritualTask])
async def get_masjid_tasks(
    id: int,
    session: Session = Depends(get_session),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
) -> List[SpiritualTask]:
    """
    Get all tasks associated with a specific masjid
    """
    masjid = session.get(Masjid, id)
    if not masjid:
        raise HTTPException(status_code=404, detail=f"Masjid with id {id} not found")

    query = select(SpiritualTask).where(SpiritualTask.masjid_id == id)

    if completed is not None:
        query = query.where(SpiritualTask.completed == completed)

    tasks = session.exec(query).all()
    return tasks


# POST /masjids - Create new masjid
@router.post("/", response_model=Masjid, status_code=201)
async def create_masjid(
    masjid_data: MasjidCreate,
    session: Session = Depends(get_session),
) -> Masjid:
    """
    Create a new masjid with prayer times
    """
    masjid = Masjid(**masjid_data.dict())
    masjid.created_at = datetime.utcnow()
    masjid.updated_at = datetime.utcnow()

    session.add(masjid)
    session.commit()
    session.refresh(masjid)
    return masjid


# PUT /masjids/{id} - Update masjid
@router.put("/{id}", response_model=Masjid)
async def update_masjid(
    id: int,
    masjid_data: MasjidUpdate,
    session: Session = Depends(get_session),
) -> Masjid:
    """
    Update an existing masjid (partial update supported)
    """
    masjid = session.get(Masjid, id)
    if not masjid:
        raise HTTPException(status_code=404, detail=f"Masjid with id {id} not found")

    update_data = masjid_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(masjid, key, value)

    masjid.updated_at = datetime.utcnow()

    session.add(masjid)
    session.commit()
    session.refresh(masjid)
    return masjid


# DELETE /masjids/{id} - Delete masjid
@router.delete("/{id}", status_code=204)
async def delete_masjid(
    id: int,
    session: Session = Depends(get_session),
) -> None:
    """
    Delete a masjid
    Note: This will set masjid_id to NULL for associated tasks (not cascade delete)
    """
    masjid = session.get(Masjid, id)
    if not masjid:
        raise HTTPException(status_code=404, detail=f"Masjid with id {id} not found")

    # Update tasks to remove masjid reference
    tasks = session.exec(select(SpiritualTask).where(SpiritualTask.masjid_id == id)).all()
    for task in tasks:
        task.masjid_id = None
        session.add(task)

    session.delete(masjid)
    session.commit()


# GET /areas - Get unique area names
@router.get("/areas/list")
async def get_areas(
    session: Session = Depends(get_session),
):
    """
    Get unique area names from masjids (for dropdown filters)
    """
    query = select(Masjid.area_name).distinct().order_by(Masjid.area_name)
    areas = session.exec(query).all()
    return {
        "areas": areas,
        "total": len(areas)
    }
