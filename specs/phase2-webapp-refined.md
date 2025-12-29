# Phase II Specification (Refined) – SalaatFlow Full-Stack Web Application

**Project**: SalaatFlow – Intelligent Prayer & Masjid Todo Assistant
**Phase**: II – Full-Stack Web Application (Refined with Masjid Backend + Theme)
**Version**: 2.0 (Refined)
**Date**: 2025-12-28
**Status**: Ready for Implementation
**Refinement Focus**: Complete Masjid Backend + Database + Black/Orange/White Theme

---

## CRITICAL REFINEMENTS IN VERSION 2.0

This refined specification addresses three critical gaps in the original Phase II spec:

1. **Complete Masjid Backend Implementation**
   - Full SQLModel database schema for Masjid entity
   - Complete CRUD API endpoints with example requests/responses
   - Database migration strategy using Alembic
   - Seed data for testing

2. **Black/Orange/White Visual Theme**
   - Comprehensive color palette and design system
   - Text visibility requirements for all UI elements
   - Input field styling with proper contrast
   - Accessible dark theme implementation

3. **Enhanced Masjid Frontend Flows**
   - Complete CRUD workflows for Masjid management
   - Prayer times management interface
   - Area-based filtering and browsing
   - Integration with Task creation workflow

---

## 1. Phase II Constitution – Full-Stack Evolution

### 1.1 Purpose
Phase II transforms the console application into a modern full-stack web application with **persistent storage**, **RESTful API**, **responsive web interface**, and **complete Masjid management**. The Masjid module is now a **first-class feature**, not optional.

### 1.2 Scope

**In Scope:**
- ✅ Persistent database storage (PostgreSQL via Neon)
- ✅ RESTful API backend (FastAPI)
- ✅ Modern web frontend (Next.js 14+ with App Router)
- ✅ All Phase I features via web UI
- ✅ Intermediate Todo features: priorities, tags, search, filter, sort
- ✅ **COMPLETE Masjid management with database backend**
- ✅ **Full CRUD operations for Masjids**
- ✅ **Prayer times management and display**
- ✅ **Area-based masjid filtering**
- ✅ Daily Hadith display
- ✅ Basic recurrence support (daily/weekly/monthly)
- ✅ **Black/Orange/White theme implementation**
- ✅ **Accessible UI with proper text contrast**

**Out of Scope:**
- AI chatbot (Phase III)
- Natural language processing
- Kubernetes deployment (Phase IV)
- Cloud deployment (Phase V)
- Advanced recurring task logic (Phase III)
- Smart reminders and notifications (Phase III)
- User authentication (optional for Phase II, required for Phase III+)

### 1.3 Tech Stack

**Backend:**
- Python 3.11+
- FastAPI 0.100+
- SQLModel 0.0.14+ (SQLAlchemy + Pydantic)
- Neon PostgreSQL (serverless Postgres)
- Alembic for database migrations
- Uvicorn (ASGI server)

**Frontend:**
- Next.js 14+ (App Router, TypeScript)
- React 18+
- TailwindCSS for styling (with custom black/orange/white theme)
- Axios for API calls
- Client-side state management

**Database:**
- PostgreSQL 15+ (via Neon)
- SQLModel for ORM
- Alembic for migrations

---

## 2. Data Models (SQLModel) – COMPLETE SPECIFICATION

### 2.1 Masjid Model (PRIMARY FOCUS)

**Table Name**: `masjids`

**Purpose**: Store complete information about masjids including location, contact details, and prayer times. This is a **required** table for Phase II.

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Masjid(SQLModel, table=True):
    """
    Masjid entity representing an Islamic prayer facility.

    This model stores complete masjid information including:
    - Identity (name, area, address)
    - Contact information (imam, phone)
    - Location coordinates (for future map features)
    - Prayer times for all 5 daily prayers plus Jummah
    - Relationships to associated spiritual tasks

    Prayer times are stored as strings in HH:MM format (24-hour).
    Future phases will implement dynamic prayer time calculation.
    """
    __tablename__ = "masjids"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core Identity - REQUIRED
    name: str = Field(
        max_length=200,
        index=True,
        description="Masjid name (e.g., 'Masjid Al-Huda')"
    )
    area_name: str = Field(
        max_length=100,
        index=True,
        description="Locality/neighborhood name for filtering (e.g., 'DHA Phase 5')"
    )

    # Location Details - OPTIONAL
    city: Optional[str] = Field(
        default=None,
        max_length=100,
        description="City name (e.g., 'Karachi')"
    )
    address: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Full street address"
    )

    # Geographic Coordinates - OPTIONAL (for Phase III maps)
    latitude: Optional[float] = Field(
        default=None,
        ge=-90.0,
        le=90.0,
        description="GPS latitude coordinate"
    )
    longitude: Optional[float] = Field(
        default=None,
        ge=-180.0,
        le=180.0,
        description="GPS longitude coordinate"
    )

    # Contact Information - OPTIONAL
    imam_name: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Name of the masjid's imam"
    )
    phone: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Contact phone number"
    )

    # Prayer Times - REQUIRED (5 daily prayers)
    # Format: HH:MM (24-hour), e.g., "05:30", "13:00"
    # Validation regex: ^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$
    fajr_time: str = Field(
        max_length=5,
        regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$",
        description="Fajr prayer time (HH:MM)"
    )
    dhuhr_time: str = Field(
        max_length=5,
        regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$",
        description="Dhuhr prayer time (HH:MM)"
    )
    asr_time: str = Field(
        max_length=5,
        regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$",
        description="Asr prayer time (HH:MM)"
    )
    maghrib_time: str = Field(
        max_length=5,
        regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$",
        description="Maghrib prayer time (HH:MM)"
    )
    isha_time: str = Field(
        max_length=5,
        regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$",
        description="Isha prayer time (HH:MM)"
    )

    # Friday Prayer - OPTIONAL
    jummah_time: Optional[str] = Field(
        default=None,
        max_length=5,
        regex=r"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$",
        description="Friday Jummah prayer time (HH:MM), optional"
    )

    # Relationships
    tasks: List["SpiritualTask"] = Relationship(
        back_populates="masjid",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    # Metadata - AUTO-MANAGED
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record creation timestamp (UTC)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Masjid Al-Huda",
                "area_name": "DHA Phase 5",
                "city": "Karachi",
                "address": "123 Main Street, DHA Phase 5",
                "imam_name": "Maulana Abdul Rahman",
                "phone": "+92-300-1234567",
                "latitude": 24.8607,
                "longitude": 67.0011,
                "fajr_time": "05:30",
                "dhuhr_time": "13:00",
                "asr_time": "16:30",
                "maghrib_time": "18:15",
                "isha_time": "19:45",
                "jummah_time": "13:30"
            }
        }
```

**Field Constraints Summary**:
| Field | Type | Required | Max Length | Indexed | Validation |
|-------|------|----------|------------|---------|------------|
| id | int | Auto | - | Primary Key | - |
| name | str | ✅ Yes | 200 | ✅ Yes | Non-empty |
| area_name | str | ✅ Yes | 100 | ✅ Yes | Non-empty |
| city | str | ❌ No | 100 | No | - |
| address | str | ❌ No | 500 | No | - |
| latitude | float | ❌ No | - | No | -90 to 90 |
| longitude | float | ❌ No | - | No | -180 to 180 |
| imam_name | str | ❌ No | 200 | No | - |
| phone | str | ❌ No | 20 | No | - |
| fajr_time | str | ✅ Yes | 5 | No | HH:MM regex |
| dhuhr_time | str | ✅ Yes | 5 | No | HH:MM regex |
| asr_time | str | ✅ Yes | 5 | No | HH:MM regex |
| maghrib_time | str | ✅ Yes | 5 | No | HH:MM regex |
| isha_time | str | ✅ Yes | 5 | No | HH:MM regex |
| jummah_time | str | ❌ No | 5 | No | HH:MM regex |
| created_at | datetime | Auto | - | No | UTC timestamp |
| updated_at | datetime | Auto | - | No | UTC timestamp |

**Business Rules**:
1. All 5 daily prayer times (Fajr, Dhuhr, Asr, Maghrib, Isha) are **mandatory**
2. Jummah time is **optional** (some masjids may not hold Friday prayers)
3. Prayer times must be in 24-hour HH:MM format (e.g., "05:30", "13:00")
4. Area name is indexed for efficient filtering by locality
5. Masjid name is indexed for search functionality
6. Deleting a masjid cascades to delete associated tasks (or can be configured to prevent deletion if tasks exist)
7. `updated_at` is automatically refreshed on any update operation

**Sample Data Rows**:

```python
# Example 1: Detailed masjid with all optional fields
{
    "id": 1,
    "name": "Masjid Al-Huda",
    "area_name": "DHA Phase 5",
    "city": "Karachi",
    "address": "123 Main Street, DHA Phase 5, Karachi",
    "imam_name": "Maulana Abdul Rahman",
    "phone": "+92-300-1234567",
    "latitude": 24.8607,
    "longitude": 67.0011,
    "fajr_time": "05:30",
    "dhuhr_time": "13:00",
    "asr_time": "16:30",
    "maghrib_time": "18:15",
    "isha_time": "19:45",
    "jummah_time": "13:30",
    "created_at": "2025-12-27T09:00:00Z",
    "updated_at": "2025-12-27T09:00:00Z"
}

# Example 2: Minimal masjid with only required fields
{
    "id": 2,
    "name": "Masjid Al-Noor",
    "area_name": "Gulshan-e-Iqbal Block 13",
    "city": null,
    "address": null,
    "imam_name": null,
    "phone": null,
    "latitude": null,
    "longitude": null,
    "fajr_time": "05:25",
    "dhuhr_time": "12:55",
    "asr_time": "16:25",
    "maghrib_time": "18:10",
    "isha_time": "19:40",
    "jummah_time": null,
    "created_at": "2025-12-27T10:00:00Z",
    "updated_at": "2025-12-27T10:00:00Z"
}

# Example 3: Masjid in different area
{
    "id": 3,
    "name": "Jamia Masjid Clifton",
    "area_name": "Clifton Block 2",
    "city": "Karachi",
    "address": "Sea View Road, Clifton",
    "imam_name": "Maulana Tariq Jameel",
    "phone": "+92-321-9876543",
    "latitude": 24.8167,
    "longitude": 67.0299,
    "fajr_time": "05:35",
    "dhuhr_time": "13:05",
    "asr_time": "16:35",
    "maghrib_time": "18:20",
    "isha_time": "19:50",
    "jummah_time": "13:15",
    "created_at": "2025-12-27T11:00:00Z",
    "updated_at": "2025-12-27T11:00:00Z"
}
```

---

### 2.2 SpiritualTask Model (Updated with Masjid FK)

**Table Name**: `spiritual_tasks`

**Changes from Original**:
- Foreign key `masjid_id` now references the **real** `masjids` table
- Relationship properly configured with cascade options

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TaskCategory(str, Enum):
    FARZ = "Farz"
    SUNNAH = "Sunnah"
    NAFL = "Nafl"
    DEED = "Deed"
    OTHER = "Other"

class Priority(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Recurrence(str, Enum):
    NONE = "None"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"

class SpiritualTask(SQLModel, table=True):
    __tablename__ = "spiritual_tasks"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Core Fields
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=2000)

    # Categorization
    category: TaskCategory = Field(default=TaskCategory.OTHER)
    priority: Priority = Field(default=Priority.MEDIUM, index=True)
    tags: Optional[str] = Field(default=None)  # JSON array stored as string

    # Masjid Association - REFERENCES REAL MASJID TABLE
    masjid_id: Optional[int] = Field(
        default=None,
        foreign_key="masjids.id",
        description="Foreign key to Masjid table"
    )
    masjid: Optional["Masjid"] = Relationship(back_populates="tasks")

    # Scheduling
    due_datetime: Optional[datetime] = Field(default=None, index=True)
    recurrence: Recurrence = Field(default=Recurrence.NONE)

    # Status
    completed: bool = Field(default=False, index=True)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Relationship Behavior**:
- **On Masjid Delete**: Configure either:
  - **Option A (Recommended)**: Set `masjid_id` to NULL (preserve tasks, orphan them)
  - **Option B**: Prevent deletion if tasks exist (raise error)
  - **Option C**: Cascade delete (remove all associated tasks)

---

### 2.3 DailyHadith Model (Unchanged)

(Same as original specification - no changes needed)

---

## 3. API Specification (FastAPI) – COMPLETE MASJID ENDPOINTS

### 3.1 Base URL & Configuration

**Base URL**: `http://localhost:8000/api/v1`

**CORS Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)
```

---

### 3.2 Masjid Endpoints (COMPLETE SPECIFICATION)

#### 3.2.1 List All Masjids

**Endpoint**: `GET /api/v1/masjids`

**Purpose**: Retrieve all masjids with optional filtering

**Query Parameters**:
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| area_name | string | No | Filter by exact area name | `DHA Phase 5` |
| search | string | No | Search in name or area (case-insensitive) | `Al-Huda` |
| limit | integer | No | Max results (default: 100, max: 500) | `20` |
| offset | integer | No | Pagination offset (default: 0) | `0` |

**Example Request**:
```bash
# List all masjids
curl -X GET "http://localhost:8000/api/v1/masjids"

# Filter by area
curl -X GET "http://localhost:8000/api/v1/masjids?area_name=DHA%20Phase%205"

# Search by name
curl -X GET "http://localhost:8000/api/v1/masjids?search=Al-Huda"

# Pagination
curl -X GET "http://localhost:8000/api/v1/masjids?limit=10&offset=0"
```

**Success Response**: `200 OK`
```json
{
  "masjids": [
    {
      "id": 1,
      "name": "Masjid Al-Huda",
      "area_name": "DHA Phase 5",
      "city": "Karachi",
      "address": "123 Main Street, DHA Phase 5",
      "imam_name": "Maulana Abdul Rahman",
      "phone": "+92-300-1234567",
      "latitude": 24.8607,
      "longitude": 67.0011,
      "fajr_time": "05:30",
      "dhuhr_time": "13:00",
      "asr_time": "16:30",
      "maghrib_time": "18:15",
      "isha_time": "19:45",
      "jummah_time": "13:30",
      "created_at": "2025-12-27T09:00:00Z",
      "updated_at": "2025-12-27T09:00:00Z"
    },
    {
      "id": 2,
      "name": "Masjid Al-Noor",
      "area_name": "Gulshan-e-Iqbal Block 13",
      "city": "Karachi",
      "address": "456 Block 13, Gulshan-e-Iqbal",
      "imam_name": null,
      "phone": null,
      "latitude": 24.9056,
      "longitude": 67.0822,
      "fajr_time": "05:25",
      "dhuhr_time": "12:55",
      "asr_time": "16:25",
      "maghrib_time": "18:10",
      "isha_time": "19:40",
      "jummah_time": "13:15",
      "created_at": "2025-12-27T10:00:00Z",
      "updated_at": "2025-12-27T10:00:00Z"
    }
  ],
  "total": 2,
  "limit": 100,
  "offset": 0
}
```

**Error Responses**:
```json
// 400 Bad Request - Invalid query parameters
{
  "detail": "Invalid limit value. Must be between 1 and 500."
}
```

**Backend Implementation** (`backend/app/routers/masjids.py`):
```python
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, col
from typing import Optional
from app.database import get_session
from app.models import Masjid

router = APIRouter(prefix="/masjids", tags=["masjids"])

@router.get("/", response_model=dict)
async def list_masjids(
    area_name: Optional[str] = Query(None, description="Filter by area name"),
    search: Optional[str] = Query(None, description="Search in name or area"),
    limit: int = Query(100, ge=1, le=500, description="Max results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    session: Session = Depends(get_session)
):
    """
    List all masjids with optional filtering and pagination.

    - Filter by area_name for locality-based browsing
    - Search across name and area fields
    - Pagination via limit/offset
    """
    query = select(Masjid)

    # Apply filters
    if area_name:
        query = query.where(col(Masjid.area_name) == area_name)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (col(Masjid.name).ilike(search_pattern)) |
            (col(Masjid.area_name).ilike(search_pattern))
        )

    # Count total before pagination
    total_query = select(func.count()).select_from(query.subquery())
    total = session.exec(total_query).one()

    # Apply pagination
    query = query.offset(offset).limit(limit)

    masjids = session.exec(query).all()

    return {
        "masjids": masjids,
        "total": total,
        "limit": limit,
        "offset": offset
    }
```

---

#### 3.2.2 Get Single Masjid

**Endpoint**: `GET /api/v1/masjids/{masjid_id}`

**Purpose**: Retrieve detailed information for a specific masjid

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| masjid_id | integer | Yes | Masjid ID |

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/masjids/1"
```

**Success Response**: `200 OK`
```json
{
  "id": 1,
  "name": "Masjid Al-Huda",
  "area_name": "DHA Phase 5",
  "city": "Karachi",
  "address": "123 Main Street, DHA Phase 5",
  "imam_name": "Maulana Abdul Rahman",
  "phone": "+92-300-1234567",
  "latitude": 24.8607,
  "longitude": 67.0011,
  "fajr_time": "05:30",
  "dhuhr_time": "13:00",
  "asr_time": "16:30",
  "maghrib_time": "18:15",
  "isha_time": "19:45",
  "jummah_time": "13:30",
  "created_at": "2025-12-27T09:00:00Z",
  "updated_at": "2025-12-27T09:00:00Z"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Masjid with ID 999 not found"
}
```

**Backend Implementation**:
```python
@router.get("/{masjid_id}", response_model=Masjid)
async def get_masjid(
    masjid_id: int,
    session: Session = Depends(get_session)
):
    """
    Get a single masjid by ID.

    Returns complete masjid information including all prayer times.
    """
    masjid = session.get(Masjid, masjid_id)

    if not masjid:
        raise HTTPException(
            status_code=404,
            detail=f"Masjid with ID {masjid_id} not found"
        )

    return masjid
```

---

#### 3.2.3 Create Masjid

**Endpoint**: `POST /api/v1/masjids`

**Purpose**: Create a new masjid with prayer times

**Request Body**:
```json
{
  "name": "Masjid Al-Noor",
  "area_name": "Gulshan-e-Iqbal Block 13",
  "city": "Karachi",
  "address": "456 Block 13, Gulshan-e-Iqbal",
  "imam_name": "Maulana Tariq",
  "phone": "+92-321-9876543",
  "latitude": 24.9056,
  "longitude": 67.0822,
  "fajr_time": "05:25",
  "dhuhr_time": "12:55",
  "asr_time": "16:25",
  "maghrib_time": "18:10",
  "isha_time": "19:40",
  "jummah_time": "13:15"
}
```

**Validation Rules**:
| Field | Required | Format/Constraints |
|-------|----------|--------------------|
| name | ✅ Yes | 1-200 characters, non-empty |
| area_name | ✅ Yes | 1-100 characters, non-empty |
| city | ❌ No | Max 100 characters |
| address | ❌ No | Max 500 characters |
| imam_name | ❌ No | Max 200 characters |
| phone | ❌ No | Max 20 characters |
| latitude | ❌ No | -90.0 to 90.0 |
| longitude | ❌ No | -180.0 to 180.0 |
| fajr_time | ✅ Yes | HH:MM format (e.g., "05:30") |
| dhuhr_time | ✅ Yes | HH:MM format |
| asr_time | ✅ Yes | HH:MM format |
| maghrib_time | ✅ Yes | HH:MM format |
| isha_time | ✅ Yes | HH:MM format |
| jummah_time | ❌ No | HH:MM format if provided |

**Time Format Validation**:
- Regex: `^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$`
- Examples: `"05:30"`, `"13:00"`, `"23:59"`
- Invalid: `"5:30"` (must be zero-padded), `"25:00"` (invalid hour)

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/masjids" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Masjid Al-Noor",
    "area_name": "Gulshan-e-Iqbal Block 13",
    "city": "Karachi",
    "fajr_time": "05:25",
    "dhuhr_time": "12:55",
    "asr_time": "16:25",
    "maghrib_time": "18:10",
    "isha_time": "19:40"
  }'
```

**Success Response**: `201 Created`
```json
{
  "id": 2,
  "name": "Masjid Al-Noor",
  "area_name": "Gulshan-e-Iqbal Block 13",
  "city": "Karachi",
  "address": null,
  "imam_name": null,
  "phone": null,
  "latitude": null,
  "longitude": null,
  "fajr_time": "05:25",
  "dhuhr_time": "12:55",
  "asr_time": "16:25",
  "maghrib_time": "18:10",
  "isha_time": "19:40",
  "jummah_time": null,
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T10:00:00Z"
}
```

**Error Response**: `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "fajr_time"],
      "msg": "string does not match regex \"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$\"",
      "type": "value_error.str.regex"
    }
  ]
}
```

**Backend Implementation**:
```python
from pydantic import BaseModel, validator
import re

class MasjidCreate(BaseModel):
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

@router.post("/", response_model=Masjid, status_code=201)
async def create_masjid(
    masjid_data: MasjidCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new masjid with prayer times.

    All 5 daily prayer times are required.
    Jummah time is optional.
    """
    masjid = Masjid(**masjid_data.dict())
    session.add(masjid)
    session.commit()
    session.refresh(masjid)

    return masjid
```

---

#### 3.2.4 Update Masjid

**Endpoint**: `PUT /api/v1/masjids/{masjid_id}`

**Purpose**: Update existing masjid information and/or prayer times

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| masjid_id | integer | Yes | Masjid ID to update |

**Request Body**: (all fields optional, only provided fields updated)
```json
{
  "fajr_time": "05:35",
  "dhuhr_time": "13:05",
  "phone": "+92-300-9999999"
}
```

**Example Request**:
```bash
# Update only prayer times
curl -X PUT "http://localhost:8000/api/v1/masjids/1" \
  -H "Content-Type: application/json" \
  -d '{
    "fajr_time": "05:35",
    "dhuhr_time": "13:05"
  }'

# Update contact information
curl -X PUT "http://localhost:8000/api/v1/masjids/1" \
  -H "Content-Type: application/json" \
  -d '{
    "imam_name": "Maulana Ahmad",
    "phone": "+92-321-5555555"
  }'
```

**Success Response**: `200 OK`
```json
{
  "id": 1,
  "name": "Masjid Al-Huda",
  "area_name": "DHA Phase 5",
  "city": "Karachi",
  "address": "123 Main Street, DHA Phase 5",
  "imam_name": "Maulana Ahmad",
  "phone": "+92-321-5555555",
  "latitude": 24.8607,
  "longitude": 67.0011,
  "fajr_time": "05:35",
  "dhuhr_time": "13:05",
  "asr_time": "16:30",
  "maghrib_time": "18:15",
  "isha_time": "19:45",
  "jummah_time": "13:30",
  "created_at": "2025-12-27T09:00:00Z",
  "updated_at": "2025-12-28T11:30:00Z"
}
```

**Error Responses**:
```json
// 404 Not Found
{
  "detail": "Masjid with ID 999 not found"
}

// 422 Validation Error
{
  "detail": [
    {
      "loc": ["body", "fajr_time"],
      "msg": "string does not match regex \"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$\"",
      "type": "value_error.str.regex"
    }
  ]
}
```

**Backend Implementation**:
```python
class MasjidUpdate(BaseModel):
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

@router.put("/{masjid_id}", response_model=Masjid)
async def update_masjid(
    masjid_id: int,
    masjid_data: MasjidUpdate,
    session: Session = Depends(get_session)
):
    """
    Update masjid information and/or prayer times.

    Only provided fields are updated. Others remain unchanged.
    The updated_at timestamp is automatically refreshed.
    """
    masjid = session.get(Masjid, masjid_id)

    if not masjid:
        raise HTTPException(
            status_code=404,
            detail=f"Masjid with ID {masjid_id} not found"
        )

    # Update only provided fields
    update_data = masjid_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(masjid, field, value)

    # Auto-update timestamp
    masjid.updated_at = datetime.utcnow()

    session.add(masjid)
    session.commit()
    session.refresh(masjid)

    return masjid
```

---

#### 3.2.5 Delete Masjid

**Endpoint**: `DELETE /api/v1/masjids/{masjid_id}`

**Purpose**: Delete a masjid (admin only)

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| masjid_id | integer | Yes | Masjid ID to delete |

**Example Request**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/masjids/1"
```

**Success Response**: `204 No Content`
(Empty response body)

**Error Responses**:
```json
// 404 Not Found
{
  "detail": "Masjid with ID 999 not found"
}

// 409 Conflict (if tasks exist and cascade delete not configured)
{
  "detail": "Cannot delete masjid. 5 task(s) are associated with this masjid. Please delete or reassign tasks first."
}
```

**Backend Implementation**:
```python
@router.delete("/{masjid_id}", status_code=204)
async def delete_masjid(
    masjid_id: int,
    session: Session = Depends(get_session)
):
    """
    Delete a masjid.

    Behavior depends on foreign key configuration:
    - CASCADE: Deletes masjid and all associated tasks
    - RESTRICT: Prevents deletion if tasks exist
    - SET NULL: Deletes masjid, sets masjid_id to NULL in tasks
    """
    masjid = session.get(Masjid, masjid_id)

    if not masjid:
        raise HTTPException(
            status_code=404,
            detail=f"Masjid with ID {masjid_id} not found"
        )

    # Optional: Check for associated tasks and prevent deletion
    task_count = session.exec(
        select(func.count()).where(SpiritualTask.masjid_id == masjid_id)
    ).one()

    if task_count > 0:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot delete masjid. {task_count} task(s) are associated with this masjid. Please delete or reassign tasks first."
        )

    session.delete(masjid)
    session.commit()

    return Response(status_code=204)
```

---

#### 3.2.6 Get Masjids by Area

**Endpoint**: `GET /api/v1/areas/{area_name}/masjids`

**Purpose**: List all masjids in a specific area (convenience endpoint)

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| area_name | string | Yes | Area name to filter by |

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/areas/DHA%20Phase%205/masjids"
```

**Success Response**: `200 OK`
```json
{
  "area_name": "DHA Phase 5",
  "masjids": [
    {
      "id": 1,
      "name": "Masjid Al-Huda",
      "area_name": "DHA Phase 5",
      "fajr_time": "05:30",
      "dhuhr_time": "13:00",
      "asr_time": "16:30",
      "maghrib_time": "18:15",
      "isha_time": "19:45",
      "jummah_time": "13:30"
    }
  ],
  "total": 1
}
```

**Backend Implementation**:
```python
@router.get("/areas/{area_name}/masjids", response_model=dict)
async def get_masjids_by_area(
    area_name: str,
    session: Session = Depends(get_session)
):
    """
    Get all masjids in a specific area.

    Convenience endpoint for area-based browsing.
    """
    query = select(Masjid).where(col(Masjid.area_name) == area_name)
    masjids = session.exec(query).all()

    return {
        "area_name": area_name,
        "masjids": masjids,
        "total": len(masjids)
    }
```

---

### 3.3 Utility Endpoints

#### 3.3.1 Get Areas List

**Endpoint**: `GET /api/v1/areas`

**Purpose**: Get unique list of area names from Masjid table (for dropdown filters)

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/areas"
```

**Success Response**: `200 OK`
```json
{
  "areas": [
    "Clifton Block 2",
    "DHA Phase 5",
    "Gulshan-e-Iqbal Block 13",
    "Malir Cantt"
  ],
  "total": 4
}
```

**Backend Implementation**:
```python
from sqlalchemy import func

@router.get("/areas", response_model=dict)
async def get_areas(session: Session = Depends(get_session)):
    """
    Get unique list of area names from masjids.

    Used to populate area filter dropdowns in frontend.
    Returns alphabetically sorted list.
    """
    query = select(Masjid.area_name).distinct().order_by(Masjid.area_name)
    areas = session.exec(query).all()

    return {
        "areas": areas,
        "total": len(areas)
    }
```

---

## 4. Database Setup & Migrations

### 4.1 Alembic Migration Strategy

**Purpose**: Manage database schema changes using Alembic migrations

**Initial Setup**:
```bash
# Install Alembic
pip install alembic

# Initialize Alembic
cd backend
alembic init alembic
```

**Configuration** (`alembic/env.py`):
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel
from alembic import context

# Import all models to ensure they're registered
from app.models import Masjid, SpiritualTask, DailyHadith

# Alembic Config object
config = context.config

# Set database URL from environment
import os
from dotenv import load_dotenv
load_dotenv()
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# SQLModel metadata
target_metadata = SQLModel.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

**Create Initial Migration**:
```bash
# Generate migration from models
alembic revision --autogenerate -m "Initial schema: masjids, spiritual_tasks, daily_hadiths"

# Review the generated migration in alembic/versions/
# Verify tables, columns, indexes, foreign keys are correct

# Apply migration to database
alembic upgrade head
```

**Expected Migration Contents**:
```python
# alembic/versions/xxxx_initial_schema.py

def upgrade():
    # Create masjids table
    op.create_table(
        'masjids',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('area_name', sa.String(length=100), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('imam_name', sa.String(length=200), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('fajr_time', sa.String(length=5), nullable=False),
        sa.Column('dhuhr_time', sa.String(length=5), nullable=False),
        sa.Column('asr_time', sa.String(length=5), nullable=False),
        sa.Column('maghrib_time', sa.String(length=5), nullable=False),
        sa.Column('isha_time', sa.String(length=5), nullable=False),
        sa.Column('jummah_time', sa.String(length=5), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_masjids_name', 'masjids', ['name'])
    op.create_index('ix_masjids_area_name', 'masjids', ['area_name'])

    # Create spiritual_tasks table
    op.create_table(
        'spiritual_tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.String(length=2000), nullable=True),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('priority', sa.String(), nullable=False),
        sa.Column('tags', sa.String(), nullable=True),
        sa.Column('masjid_id', sa.Integer(), nullable=True),
        sa.Column('due_datetime', sa.DateTime(), nullable=True),
        sa.Column('recurrence', sa.String(), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['masjid_id'], ['masjids.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_spiritual_tasks_title', 'spiritual_tasks', ['title'])
    op.create_index('ix_spiritual_tasks_priority', 'spiritual_tasks', ['priority'])
    op.create_index('ix_spiritual_tasks_completed', 'spiritual_tasks', ['completed'])
    op.create_index('ix_spiritual_tasks_due_datetime', 'spiritual_tasks', ['due_datetime'])

    # Create daily_hadiths table
    op.create_table(
        'daily_hadiths',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(length=2000), nullable=False),
        sa.Column('reference', sa.String(length=200), nullable=False),
        sa.Column('language', sa.String(length=5), nullable=False),
        sa.Column('display_date', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_daily_hadiths_display_date', 'daily_hadiths', ['display_date'])

def downgrade():
    op.drop_table('spiritual_tasks')
    op.drop_table('masjids')
    op.drop_table('daily_hadiths')
```

---

### 4.2 Seed Data Script

**Purpose**: Populate database with sample masjids, tasks, and hadiths for testing

**File**: `backend/seed.py`

```python
"""
Seed script for SalaatFlow Phase II database.

Populates the database with:
- 10 sample masjids across different Karachi areas
- 30 sample spiritual tasks with variety
- 7 daily hadiths for the upcoming week

Usage:
    python seed.py
"""

from sqlmodel import Session, create_engine, select
from app.models import Masjid, SpiritualTask, DailyHadith, TaskCategory, Priority, Recurrence
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def seed_masjids(session: Session):
    """Seed sample masjids across Karachi areas."""

    masjids_data = [
        {
            "name": "Masjid Al-Huda",
            "area_name": "DHA Phase 5",
            "city": "Karachi",
            "address": "123 Main Street, DHA Phase 5",
            "imam_name": "Maulana Abdul Rahman",
            "phone": "+92-300-1234567",
            "latitude": 24.8607,
            "longitude": 67.0011,
            "fajr_time": "05:30",
            "dhuhr_time": "13:00",
            "asr_time": "16:30",
            "maghrib_time": "18:15",
            "isha_time": "19:45",
            "jummah_time": "13:30"
        },
        {
            "name": "Masjid Al-Noor",
            "area_name": "Gulshan-e-Iqbal Block 13",
            "city": "Karachi",
            "address": "456 Block 13, Gulshan-e-Iqbal",
            "imam_name": "Maulana Tariq Jameel",
            "phone": "+92-321-9876543",
            "latitude": 24.9056,
            "longitude": 67.0822,
            "fajr_time": "05:25",
            "dhuhr_time": "12:55",
            "asr_time": "16:25",
            "maghrib_time": "18:10",
            "isha_time": "19:40",
            "jummah_time": "13:15"
        },
        {
            "name": "Jamia Masjid Clifton",
            "area_name": "Clifton Block 2",
            "city": "Karachi",
            "address": "Sea View Road, Clifton",
            "imam_name": "Maulana Ahmad Shah",
            "phone": "+92-333-5555555",
            "latitude": 24.8167,
            "longitude": 67.0299,
            "fajr_time": "05:35",
            "dhuhr_time": "13:05",
            "asr_time": "16:35",
            "maghrib_time": "18:20",
            "isha_time": "19:50",
            "jummah_time": "13:15"
        },
        {
            "name": "Masjid Bilal",
            "area_name": "Malir Cantt",
            "city": "Karachi",
            "address": "Malir Cantonment Area",
            "imam_name": None,
            "phone": None,
            "latitude": 24.9431,
            "longitude": 67.2091,
            "fajr_time": "05:20",
            "dhuhr_time": "12:50",
            "asr_time": "16:20",
            "maghrib_time": "18:05",
            "isha_time": "19:35",
            "jummah_time": None
        },
        {
            "name": "Masjid-e-Tooba",
            "area_name": "Defence Phase 2",
            "city": "Karachi",
            "address": "Korangi Road, DHA Phase 2",
            "imam_name": "Maulana Zubair Hassan",
            "phone": "+92-300-7777777",
            "latitude": 24.8138,
            "longitude": 67.0722,
            "fajr_time": "05:30",
            "dhuhr_time": "13:00",
            "asr_time": "16:30",
            "maghrib_time": "18:15",
            "isha_time": "19:45",
            "jummah_time": "12:30"
        },
        {
            "name": "Masjid Ayesha",
            "area_name": "North Nazimabad Block B",
            "city": "Karachi",
            "address": "Block B, North Nazimabad",
            "imam_name": "Maulana Saeed Ahmed",
            "phone": "+92-321-4444444",
            "latitude": 24.9267,
            "longitude": 67.0397,
            "fajr_time": "05:28",
            "dhuhr_time": "12:58",
            "asr_time": "16:28",
            "maghrib_time": "18:13",
            "isha_time": "19:43",
            "jummah_time": "13:00"
        },
        {
            "name": "Masjid Ibrahim",
            "area_name": "Saddar Town",
            "city": "Karachi",
            "address": "Abdullah Haroon Road, Saddar",
            "imam_name": None,
            "phone": "+92-333-2222222",
            "latitude": 24.8546,
            "longitude": 67.0231,
            "fajr_time": "05:32",
            "dhuhr_time": "13:02",
            "asr_time": "16:32",
            "maghrib_time": "18:17",
            "isha_time": "19:47",
            "jummah_time": "13:30"
        },
        {
            "name": "Masjid Umar",
            "area_name": "Korangi Industrial Area",
            "city": "Karachi",
            "address": "Korangi Industrial Area, Sector 23",
            "imam_name": "Maulana Rashid Khan",
            "phone": None,
            "latitude": 24.8607,
            "longitude": 67.1520,
            "fajr_time": "05:22",
            "dhuhr_time": "12:52",
            "asr_time": "16:22",
            "maghrib_time": "18:07",
            "isha_time": "19:37",
            "jummah_time": "13:10"
        },
        {
            "name": "Masjid Fatima",
            "area_name": "Gulistan-e-Johar Block 15",
            "city": "Karachi",
            "address": "Block 15, Gulistan-e-Johar",
            "imam_name": "Maulana Khalid Mahmood",
            "phone": "+92-300-6666666",
            "latitude": 24.9191,
            "longitude": 67.1341,
            "fajr_time": "05:26",
            "dhuhr_time": "12:56",
            "asr_time": "16:26",
            "maghrib_time": "18:11",
            "isha_time": "19:41",
            "jummah_time": "13:20"
        },
        {
            "name": "Baitul Mukarram Masjid",
            "area_name": "Bahadurabad",
            "city": "Karachi",
            "address": "Shahrah-e-Faisal, Bahadurabad",
            "imam_name": "Maulana Ishaq Ali",
            "phone": "+92-321-8888888",
            "latitude": 24.8975,
            "longitude": 67.0675,
            "fajr_time": "05:29",
            "dhuhr_time": "12:59",
            "asr_time": "16:29",
            "maghrib_time": "18:14",
            "isha_time": "19:44",
            "jummah_time": "13:00"
        }
    ]

    for masjid_data in masjids_data:
        masjid = Masjid(**masjid_data)
        session.add(masjid)

    session.commit()
    print(f"✅ Seeded {len(masjids_data)} masjids")

def seed_tasks(session: Session):
    """Seed sample spiritual tasks linked to masjids."""

    # Get masjids for foreign key references
    masjids = session.exec(select(Masjid)).all()
    masjid_ids = [m.id for m in masjids]

    tasks_data = [
        {
            "title": "Attend Fajr at Masjid Al-Huda",
            "description": "Wake up 30 minutes early for preparation",
            "category": TaskCategory.FARZ,
            "priority": Priority.HIGH,
            "tags": "Fajr,Masjid",
            "masjid_id": masjid_ids[0] if len(masjid_ids) > 0 else None,
            "due_datetime": datetime.now() + timedelta(days=1, hours=5, minutes=30),
            "recurrence": Recurrence.DAILY,
            "completed": False
        },
        {
            "title": "Read Surah Yaseen after Fajr",
            "description": "Complete Surah Yaseen with translation",
            "category": TaskCategory.SUNNAH,
            "priority": Priority.MEDIUM,
            "tags": "Quran,Morning",
            "masjid_id": None,
            "due_datetime": datetime.now() + timedelta(days=1, hours=6),
            "recurrence": Recurrence.DAILY,
            "completed": False
        },
        {
            "title": "Donate to Masjid Al-Noor",
            "description": "Monthly charity contribution",
            "category": TaskCategory.DEED,
            "priority": Priority.MEDIUM,
            "tags": "Charity,Sadaqah",
            "masjid_id": masjid_ids[1] if len(masjid_ids) > 1 else None,
            "due_datetime": datetime.now() + timedelta(days=7),
            "recurrence": Recurrence.MONTHLY,
            "completed": False
        },
        {
            "title": "Attend Jummah at Jamia Masjid Clifton",
            "description": "Leave early to avoid traffic",
            "category": TaskCategory.FARZ,
            "priority": Priority.HIGH,
            "tags": "Jummah,Friday",
            "masjid_id": masjid_ids[2] if len(masjid_ids) > 2 else None,
            "due_datetime": datetime.now() + timedelta(days=3, hours=13, minutes=15),
            "recurrence": Recurrence.WEEKLY,
            "completed": False
        },
        {
            "title": "Memorize Surah Al-Mulk",
            "description": "Learn 5 verses per day",
            "category": TaskCategory.NAFL,
            "priority": Priority.LOW,
            "tags": "Quran,Memorization",
            "masjid_id": None,
            "due_datetime": None,
            "recurrence": Recurrence.DAILY,
            "completed": False
        },
        # Add more varied tasks...
    ]

    for task_data in tasks_data:
        task = SpiritualTask(**task_data)
        session.add(task)

    session.commit()
    print(f"✅ Seeded {len(tasks_data)} tasks")

def seed_hadiths(session: Session):
    """Seed daily hadiths for the upcoming week."""

    hadiths_data = [
        {
            "content": "The best of people are those who are most beneficial to people.",
            "reference": "Sahih al-Jami 3289",
            "language": "en",
            "display_date": datetime.now()
        },
        {
            "content": "The strong person is not the one who can wrestle someone else down. The strong person is the one who can control himself when he is angry.",
            "reference": "Sahih Bukhari 6114",
            "language": "en",
            "display_date": datetime.now() + timedelta(days=1)
        },
        # Add more hadiths for each day of the week...
    ]

    for hadith_data in hadiths_data:
        hadith = DailyHadith(**hadith_data)
        session.add(hadith)

    session.commit()
    print(f"✅ Seeded {len(hadiths_data)} hadiths")

def main():
    """Run all seed functions."""
    print("🌱 Starting database seeding...")

    with Session(engine) as session:
        # Check if data already exists
        existing_masjids = session.exec(select(Masjid)).first()
        if existing_masjids:
            print("⚠️  Database already contains data. Skipping seed.")
            return

        seed_masjids(session)
        seed_tasks(session)
        seed_hadiths(session)

    print("✅ Database seeding complete!")

if __name__ == "__main__":
    main()
```

**Run Seed Script**:
```bash
cd backend
python seed.py
```

---

## 5. Frontend – Black/Orange/White Theme Specification

### 5.1 Color Palette & Design System

**PRIMARY THEME**: Black, Orange, White

**Color Constants** (`frontend/lib/colors.ts`):
```typescript
export const theme = {
  // Primary Colors
  black: {
    DEFAULT: '#000000',
    soft: '#0A0A0A',      // Very dark gray (backgrounds)
    light: '#1A1A1A',     // Dark gray (cards on black)
    text: '#FFFFFF',       // White text on black
  },

  orange: {
    DEFAULT: '#FF6B35',    // Primary orange (buttons, links, highlights)
    light: '#FF8C61',      // Lighter orange (hover states)
    dark: '#E05A2C',       // Darker orange (active states)
    pale: '#FFF4F0',       // Very light orange (backgrounds)
  },

  white: {
    DEFAULT: '#FFFFFF',
    soft: '#F5F5F5',       // Off-white (card backgrounds)
    gray: '#E5E5E5',       // Light gray (borders)
    text: '#000000',       // Black text on white
  },

  // Functional Colors
  success: '#10B981',      // Green for completed tasks
  warning: '#F59E0B',      // Amber for medium priority
  danger: '#EF4444',       // Red for high priority
  info: '#3B82F6',         // Blue for information

  // Text Colors
  text: {
    primary: '#FFFFFF',    // White text (on dark backgrounds)
    secondary: '#B3B3B3',  // Light gray text (less emphasis)
    dark: '#000000',       // Black text (on white backgrounds)
    muted: '#666666',      // Dark gray text (on white backgrounds)
  },

  // Prayer Time Colors (Color-coded cards - same as current)
  prayer: {
    fajr: {
      from: 'from-indigo-50',
      to: 'to-blue-50',
      text: 'text-indigo-700',
      border: 'border-indigo-200'
    },
    dhuhr: {
      from: 'from-yellow-50',
      to: 'to-orange-50',
      text: 'text-orange-700',
      border: 'border-orange-200'
    },
    asr: {
      from: 'from-amber-50',
      to: 'to-yellow-50',
      text: 'text-amber-700',
      border: 'border-amber-200'
    },
    maghrib: {
      from: 'from-rose-50',
      to: 'to-pink-50',
      text: 'text-rose-700',
      border: 'border-rose-200'
    },
    isha: {
      from: 'from-purple-50',
      to: 'to-indigo-50',
      text: 'text-purple-700',
      border: 'border-purple-200'
    },
    jummah: {
      from: 'from-emerald-50',
      to: 'to-green-50',
      text: 'text-emerald-700',
      border: 'border-emerald-200'
    }
  }
};
```

**Tailwind Configuration** (`tailwind.config.ts`):
```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'salaat-black': {
          DEFAULT: '#000000',
          soft: '#0A0A0A',
          light: '#1A1A1A',
        },
        'salaat-orange': {
          DEFAULT: '#FF6B35',
          light: '#FF8C61',
          dark: '#E05A2C',
          pale: '#FFF4F0',
        },
        'salaat-white': {
          DEFAULT: '#FFFFFF',
          soft: '#F5F5F5',
          gray: '#E5E5E5',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        arabic: ['Amiri', 'serif'], // For Islamic text
      },
    },
  },
  plugins: [],
}

export default config
```

---

### 5.2 Global Layout Theme

**Root Layout** (`app/layout.tsx`):
```tsx
import Navbar from '@/components/Navbar'
import './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-salaat-black-soft min-h-screen text-salaat-black-text">
        {/* Navbar with black/orange theme */}
        <Navbar />

        {/* Main content area */}
        <main className="min-h-screen">
          {children}
        </main>
      </body>
    </html>
  )
}
```

**Global Styles** (`app/globals.css`):
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  /* Default body - dark background, white text */
  body {
    @apply bg-salaat-black-soft text-white;
  }

  /* Headings */
  h1, h2, h3, h4, h5, h6 {
    @apply font-bold text-white;
  }

  /* Links */
  a {
    @apply text-salaat-orange hover:text-salaat-orange-light transition-colors;
  }

  /* Scrollbar styling for dark theme */
  ::-webkit-scrollbar {
    @apply w-2;
  }

  ::-webkit-scrollbar-track {
    @apply bg-salaat-black-light;
  }

  ::-webkit-scrollbar-thumb {
    @apply bg-salaat-orange rounded;
  }

  ::-webkit-scrollbar-thumb:hover {
    @apply bg-salaat-orange-light;
  }
}

@layer components {
  /* Card component on dark background */
  .card-dark {
    @apply bg-salaat-black-light rounded-lg shadow-lg p-6 border border-gray-800;
  }

  /* Card component on white background */
  .card-light {
    @apply bg-white rounded-lg shadow-md p-6 border border-salaat-white-gray;
  }

  /* Primary button (orange) */
  .btn-primary {
    @apply px-6 py-3 bg-salaat-orange text-white font-medium rounded-lg
           hover:bg-salaat-orange-light active:bg-salaat-orange-dark
           focus:outline-none focus:ring-2 focus:ring-salaat-orange focus:ring-offset-2 focus:ring-offset-salaat-black-soft
           transition-colors disabled:opacity-50 disabled:cursor-not-allowed;
  }

  /* Secondary button (white/gray) */
  .btn-secondary {
    @apply px-6 py-3 bg-gray-700 text-white font-medium rounded-lg
           hover:bg-gray-600 active:bg-gray-800
           focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:ring-offset-salaat-black-soft
           transition-colors;
  }

  /* Input fields - CRITICAL: Proper text visibility */
  .input-field {
    @apply w-full px-4 py-3 bg-salaat-black-light text-white
           border border-gray-700 rounded-lg
           placeholder-gray-500
           focus:outline-none focus:ring-2 focus:ring-salaat-orange focus:border-transparent
           disabled:opacity-50 disabled:cursor-not-allowed;
  }

  /* Input fields on white background (for modal/popup forms) */
  .input-field-light {
    @apply w-full px-4 py-3 bg-white text-black
           border border-salaat-white-gray rounded-lg
           placeholder-gray-400
           focus:outline-none focus:ring-2 focus:ring-salaat-orange focus:border-transparent;
  }

  /* Label styling */
  .label-field {
    @apply block text-sm font-medium text-white mb-2;
  }

  .label-field-light {
    @apply block text-sm font-medium text-black mb-2;
  }

  /* Select/Dropdown styling */
  .select-field {
    @apply input-field cursor-pointer;
  }

  /* Textarea styling */
  .textarea-field {
    @apply input-field resize-vertical min-h-[100px];
  }
}
```

---

### 5.3 Navbar Component (Black/Orange Theme)

**Component** (`components/Navbar.tsx`):
```tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState } from 'react'

export default function Navbar() {
  const pathname = usePathname()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const navLinks = [
    { href: '/', label: 'Dashboard', icon: '🏠' },
    { href: '/tasks', label: 'Tasks', icon: '✓' },
    { href: '/masjids', label: 'Masjids', icon: '🕌' },
    { href: '/hadith', label: 'Daily Hadith', icon: '📖' },
  ]

  const isActive = (href: string) => pathname === href

  return (
    <nav className="bg-black border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
            <span className="text-3xl">🕌</span>
            <span className="text-xl font-bold">
              <span className="text-white">Salaat</span>
              <span className="text-salaat-orange">Flow</span>
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`
                  flex items-center px-4 py-2 rounded-md text-sm font-medium transition-colors
                  ${isActive(link.href)
                    ? 'bg-salaat-orange text-white shadow-md'
                    : 'text-gray-300 hover:bg-gray-900 hover:text-salaat-orange'
                  }
                `}
              >
                <span className="mr-2">{link.icon}</span>
                {link.label}
              </Link>
            ))}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-salaat-orange hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-salaat-orange"
              aria-label="Toggle menu"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-salaat-black-light border-t border-gray-800">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`
                  flex items-center px-3 py-2 rounded-md text-base font-medium transition-colors
                  ${isActive(link.href)
                    ? 'bg-salaat-orange text-white'
                    : 'text-gray-300 hover:bg-gray-900 hover:text-salaat-orange'
                  }
                `}
              >
                <span className="mr-3">{link.icon}</span>
                {link.label}
              </Link>
            ))}
          </div>
        </div>
      )}
    </nav>
  )
}
```

---

### 5.4 Input Field Components (Text Visibility Fix)

**CRITICAL ISSUE**: Original implementation had poor text visibility in input fields

**Form Input Component** (`components/FormInput.tsx`):
```tsx
interface FormInputProps {
  label: string
  name: string
  type?: 'text' | 'email' | 'tel' | 'time' | 'date' | 'datetime-local'
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  placeholder?: string
  required?: boolean
  error?: string
  disabled?: boolean
}

export default function FormInput({
  label,
  name,
  type = 'text',
  value,
  onChange,
  placeholder,
  required = false,
  error,
  disabled = false,
}: FormInputProps) {
  return (
    <div className="mb-4">
      {/* Label - WHITE text on dark background */}
      <label htmlFor={name} className="label-field">
        {label}
        {required && <span className="text-salaat-orange ml-1">*</span>}
      </label>

      {/* Input - WHITE text, DARK background, LIGHT border */}
      <input
        type={type}
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        disabled={disabled}
        className={`
          input-field
          ${error ? 'border-red-500 focus:ring-red-500' : ''}
        `}
      />

      {/* Error message - RED text */}
      {error && (
        <p className="mt-2 text-sm text-red-400">
          {error}
        </p>
      )}
    </div>
  )
}
```

**Textarea Component** (`components/FormTextarea.tsx`):
```tsx
interface FormTextareaProps {
  label: string
  name: string
  value: string
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void
  placeholder?: string
  required?: boolean
  error?: string
  rows?: number
}

export default function FormTextarea({
  label,
  name,
  value,
  onChange,
  placeholder,
  required = false,
  error,
  rows = 4,
}: FormTextareaProps) {
  return (
    <div className="mb-4">
      <label htmlFor={name} className="label-field">
        {label}
        {required && <span className="text-salaat-orange ml-1">*</span>}
      </label>

      <textarea
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        rows={rows}
        className={`
          textarea-field
          ${error ? 'border-red-500 focus:ring-red-500' : ''}
        `}
      />

      {error && (
        <p className="mt-2 text-sm text-red-400">
          {error}
        </p>
      )}
    </div>
  )
}
```

**Select Component** (`components/FormSelect.tsx`):
```tsx
interface FormSelectProps {
  label: string
  name: string
  value: string | number
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void
  options: { value: string | number; label: string }[]
  required?: boolean
  error?: string
}

export default function FormSelect({
  label,
  name,
  value,
  onChange,
  options,
  required = false,
  error,
}: FormSelectProps) {
  return (
    <div className="mb-4">
      <label htmlFor={name} className="label-field">
        {label}
        {required && <span className="text-salaat-orange ml-1">*</span>}
      </label>

      <select
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        required={required}
        className={`
          select-field
          ${error ? 'border-red-500 focus:ring-red-500' : ''}
        `}
      >
        <option value="" className="bg-salaat-black-light text-white">
          -- Select {label} --
        </option>
        {options.map((option) => (
          <option
            key={option.value}
            value={option.value}
            className="bg-salaat-black-light text-white"
          >
            {option.label}
          </option>
        ))}
      </select>

      {error && (
        <p className="mt-2 text-sm text-red-400">
          {error}
        </p>
      )}
    </div>
  )
}
```

---

### 5.5 Masjid Creation Form (Complete with Theme)

**Page** (`app/masjids/new/page.tsx`):
```tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import FormInput from '@/components/FormInput'
import FormTextarea from '@/components/FormTextarea'

interface MasjidFormData {
  name: string
  area_name: string
  city: string
  address: string
  imam_name: string
  phone: string
  fajr_time: string
  dhuhr_time: string
  asr_time: string
  maghrib_time: string
  isha_time: string
  jummah_time: string
}

export default function NewMasjidPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [errors, setErrors] = useState<Record<string, string>>({})

  const [formData, setFormData] = useState<MasjidFormData>({
    name: '',
    area_name: '',
    city: '',
    address: '',
    imam_name: '',
    phone: '',
    fajr_time: '',
    dhuhr_time: '',
    asr_time: '',
    maghrib_time: '',
    isha_time: '',
    jummah_time: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {}

    // Required fields
    if (!formData.name.trim()) {
      newErrors.name = 'Masjid name is required'
    }
    if (!formData.area_name.trim()) {
      newErrors.area_name = 'Area is required'
    }

    // Prayer times validation (HH:MM format)
    const timeRegex = /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/
    const requiredTimes = ['fajr_time', 'dhuhr_time', 'asr_time', 'maghrib_time', 'isha_time']

    requiredTimes.forEach(field => {
      const value = formData[field as keyof MasjidFormData]
      if (!value || !timeRegex.test(value)) {
        newErrors[field] = 'Valid time required (HH:MM format, e.g., "05:30")'
      }
    })

    // Optional jummah time validation
    if (formData.jummah_time && !timeRegex.test(formData.jummah_time)) {
      newErrors.jummah_time = 'Valid time required (HH:MM format)'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validate()) {
      setError('Please fix the errors above')
      return
    }

    try {
      setLoading(true)
      setError(null)

      const response = await fetch('http://localhost:8000/api/v1/masjids', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to create masjid')
      }

      router.push('/masjids')
    } catch (err: any) {
      console.error('Error creating masjid:', err)
      setError(err.message || 'Failed to create masjid. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-salaat-black-soft py-8 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/masjids"
            className="inline-flex items-center text-salaat-orange hover:text-salaat-orange-light mb-4"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Masjids
          </Link>

          <h1 className="text-4xl font-bold text-white mb-2">Add New Masjid</h1>
          <p className="text-gray-400">
            Create a new masjid with prayer times and location details
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded-lg">
            <p className="font-medium">Error</p>
            <p className="text-sm">{error}</p>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="card-dark space-y-6">
          {/* Section 1: Basic Information */}
          <div>
            <h2 className="text-2xl font-bold text-white mb-4 pb-2 border-b border-gray-700">
              Basic Information
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormInput
                label="Masjid Name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="e.g., Masjid Al-Huda"
                required
                error={errors.name}
              />

              <FormInput
                label="Area"
                name="area_name"
                value={formData.area_name}
                onChange={handleChange}
                placeholder="e.g., DHA Phase 5"
                required
                error={errors.area_name}
              />

              <FormInput
                label="City"
                name="city"
                value={formData.city}
                onChange={handleChange}
                placeholder="e.g., Karachi"
                error={errors.city}
              />

              <FormInput
                label="Phone"
                name="phone"
                type="tel"
                value={formData.phone}
                onChange={handleChange}
                placeholder="e.g., +92-300-1234567"
                error={errors.phone}
              />
            </div>

            <FormTextarea
              label="Address"
              name="address"
              value={formData.address}
              onChange={handleChange}
              placeholder="Full street address"
              rows={3}
              error={errors.address}
            />

            <FormInput
              label="Imam Name"
              name="imam_name"
              value={formData.imam_name}
              onChange={handleChange}
              placeholder="e.g., Maulana Abdul Rahman"
              error={errors.imam_name}
            />
          </div>

          {/* Section 2: Prayer Times */}
          <div>
            <h2 className="text-2xl font-bold text-white mb-4 pb-2 border-b border-gray-700">
              Prayer Times
            </h2>
            <p className="text-gray-400 text-sm mb-4">
              Enter times in 24-hour format (HH:MM), e.g., "05:30" or "13:00"
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <FormInput
                label="Fajr"
                name="fajr_time"
                type="time"
                value={formData.fajr_time}
                onChange={handleChange}
                placeholder="05:30"
                required
                error={errors.fajr_time}
              />

              <FormInput
                label="Dhuhr"
                name="dhuhr_time"
                type="time"
                value={formData.dhuhr_time}
                onChange={handleChange}
                placeholder="13:00"
                required
                error={errors.dhuhr_time}
              />

              <FormInput
                label="Asr"
                name="asr_time"
                type="time"
                value={formData.asr_time}
                onChange={handleChange}
                placeholder="16:30"
                required
                error={errors.asr_time}
              />

              <FormInput
                label="Maghrib"
                name="maghrib_time"
                type="time"
                value={formData.maghrib_time}
                onChange={handleChange}
                placeholder="18:15"
                required
                error={errors.maghrib_time}
              />

              <FormInput
                label="Isha"
                name="isha_time"
                type="time"
                value={formData.isha_time}
                onChange={handleChange}
                placeholder="19:45"
                required
                error={errors.isha_time}
              />

              <FormInput
                label="Jummah (Optional)"
                name="jummah_time"
                type="time"
                value={formData.jummah_time}
                onChange={handleChange}
                placeholder="13:30"
                error={errors.jummah_time}
              />
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-700">
            <Link
              href="/masjids"
              className="px-6 py-3 bg-gray-700 text-white font-medium rounded-lg hover:bg-gray-600 transition-colors"
            >
              Cancel
            </Link>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary"
            >
              {loading ? (
                <span className="flex items-center">
                  <svg className="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Creating...
                </span>
              ) : (
                'Create Masjid'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
```

---

### 5.6 Design Requirements Summary

**Page Background**:
- All pages: `bg-salaat-black-soft` (very dark gray/black)
- Ensures consistent dark theme

**Card/Content Surfaces**:
- Dark cards: `bg-salaat-black-light` (slightly lighter than background)
- White cards (if needed): `bg-white` with dark text

**Text Visibility** (CRITICAL):
| Context | Background | Text Color | CSS Class |
|---------|------------|------------|-----------|
| Page body | Black/Dark | White | `text-white` |
| Dark cards | Dark gray | White | `text-white` |
| White cards | White | Black | `text-black` |
| Input fields (dark) | Dark gray | White | `text-white` |
| Input placeholders | Dark gray | Light gray | `placeholder-gray-500` |
| Labels (dark theme) | Transparent | White | `text-white` |
| Error messages | Transparent | Red | `text-red-400` |

**Buttons**:
| Type | Background | Text | Hover | CSS Class |
|------|------------|------|-------|-----------|
| Primary | Orange | White | Light orange | `btn-primary` |
| Secondary | Gray | White | Lighter gray | `btn-secondary` |
| Danger | Red | White | Lighter red | Custom |

**Borders & Dividers**:
- On dark backgrounds: `border-gray-800` or `border-gray-700`
- On white backgrounds: `border-salaat-white-gray`

**Focus States**:
- Ring color: `ring-salaat-orange`
- Ring offset: `ring-offset-salaat-black-soft`

---

## 6. Backend File Structure

**Complete Backend Organization**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── database.py                # Database connection & session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── masjid.py             # Masjid SQLModel
│   │   ├── spiritual_task.py     # SpiritualTask SQLModel
│   │   └── daily_hadith.py       # DailyHadith SQLModel
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── masjid.py             # Pydantic schemas (Create, Update)
│   │   ├── task.py               # Task schemas
│   │   └── hadith.py             # Hadith schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── masjids.py            # Masjid CRUD endpoints
│   │   ├── tasks.py              # Task CRUD endpoints
│   │   ├── hadiths.py            # Hadith endpoints
│   │   └── utils.py              # Utility endpoints (areas, health)
│   └── crud/
│       ├── __init__.py
│       ├── masjid.py             # Masjid database operations
│       ├── task.py               # Task database operations
│       └── hadith.py             # Hadith database operations
├── alembic/
│   ├── versions/
│   │   └── xxxx_initial_schema.py
│   ├── env.py
│   └── alembic.ini
├── seed.py                        # Database seed script
├── .env                           # Environment variables
├── requirements.txt
└── README.md
```

---

## 7. Acceptance Criteria (Updated)

### 7.1 Backend - Masjid API Tests

**Test Suite**: `tests/test_masjid_api.py`

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_masjid_success():
    """Test creating a masjid with all required fields."""
    payload = {
        "name": "Test Masjid",
        "area_name": "Test Area",
        "fajr_time": "05:30",
        "dhuhr_time": "13:00",
        "asr_time": "16:30",
        "maghrib_time": "18:15",
        "isha_time": "19:45"
    }
    response = client.post("/api/v1/masjids", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Masjid"
    assert data["area_name"] == "Test Area"
    assert "id" in data

def test_create_masjid_missing_required_field():
    """Test creating masjid without required field fails."""
    payload = {
        "name": "Test Masjid",
        # Missing area_name
        "fajr_time": "05:30",
        "dhuhr_time": "13:00",
        "asr_time": "16:30",
        "maghrib_time": "18:15",
        "isha_time": "19:45"
    }
    response = client.post("/api/v1/masjids", json=payload)
    assert response.status_code == 422

def test_create_masjid_invalid_time_format():
    """Test creating masjid with invalid time format fails."""
    payload = {
        "name": "Test Masjid",
        "area_name": "Test Area",
        "fajr_time": "5:30",  # Invalid: not zero-padded
        "dhuhr_time": "13:00",
        "asr_time": "16:30",
        "maghrib_time": "18:15",
        "isha_time": "19:45"
    }
    response = client.post("/api/v1/masjids", json=payload)
    assert response.status_code == 422

def test_list_masjids():
    """Test listing all masjids."""
    response = client.get("/api/v1/masjids")
    assert response.status_code == 200
    data = response.json()
    assert "masjids" in data
    assert "total" in data
    assert isinstance(data["masjids"], list)

def test_filter_masjids_by_area():
    """Test filtering masjids by area."""
    response = client.get("/api/v1/masjids?area_name=DHA Phase 5")
    assert response.status_code == 200
    data = response.json()
    for masjid in data["masjids"]:
        assert masjid["area_name"] == "DHA Phase 5"

def test_get_single_masjid():
    """Test getting a single masjid by ID."""
    # Create masjid first
    create_response = client.post("/api/v1/masjids", json={
        "name": "Test Masjid",
        "area_name": "Test Area",
        "fajr_time": "05:30",
        "dhuhr_time": "13:00",
        "asr_time": "16:30",
        "maghrib_time": "18:15",
        "isha_time": "19:45"
    })
    masjid_id = create_response.json()["id"]

    # Get masjid
    response = client.get(f"/api/v1/masjids/{masjid_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == masjid_id
    assert data["name"] == "Test Masjid"

def test_get_nonexistent_masjid():
    """Test getting non-existent masjid returns 404."""
    response = client.get("/api/v1/masjids/99999")
    assert response.status_code == 404

def test_update_masjid_prayer_times():
    """Test updating masjid prayer times."""
    # Create masjid
    create_response = client.post("/api/v1/masjids", json={
        "name": "Test Masjid",
        "area_name": "Test Area",
        "fajr_time": "05:30",
        "dhuhr_time": "13:00",
        "asr_time": "16:30",
        "maghrib_time": "18:15",
        "isha_time": "19:45"
    })
    masjid_id = create_response.json()["id"]

    # Update prayer times
    update_response = client.put(f"/api/v1/masjids/{masjid_id}", json={
        "fajr_time": "05:35",
        "dhuhr_time": "13:05"
    })
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["fajr_time"] == "05:35"
    assert data["dhuhr_time"] == "13:05"
    assert data["asr_time"] == "16:30"  # Unchanged

def test_delete_masjid():
    """Test deleting a masjid."""
    # Create masjid
    create_response = client.post("/api/v1/masjids", json={
        "name": "Test Masjid",
        "area_name": "Test Area",
        "fajr_time": "05:30",
        "dhuhr_time": "13:00",
        "asr_time": "16:30",
        "maghrib_time": "18:15",
        "isha_time": "19:45"
    })
    masjid_id = create_response.json()["id"]

    # Delete masjid
    delete_response = client.delete(f"/api/v1/masjids/{masjid_id}")
    assert delete_response.status_code == 204

    # Verify deleted
    get_response = client.get(f"/api/v1/masjids/{masjid_id}")
    assert get_response.status_code == 404

def test_get_areas_list():
    """Test getting unique areas list."""
    response = client.get("/api/v1/areas")
    assert response.status_code == 200
    data = response.json()
    assert "areas" in data
    assert isinstance(data["areas"], list)
```

---

### 7.2 Frontend - Masjid UI Tests

**Manual Test Checklist**:

#### Masjid List Page (`/masjids`)
- [ ] Page loads with black background and white text
- [ ] "Add Masjid" button is orange and visible
- [ ] Area filter dropdown shows unique areas
- [ ] Filtering by area works correctly
- [ ] Masjid cards display name, area, and prayer times
- [ ] Click on masjid card navigates to detail page
- [ ] Text is readable (white on dark background)

#### Masjid Creation Page (`/masjids/new`)
- [ ] Form loads with dark theme
- [ ] All input fields have white text on dark background
- [ ] Placeholders are visible (light gray)
- [ ] Labels are white and visible
- [ ] Typing in inputs shows white text clearly
- [ ] Time inputs work correctly (HH:MM format)
- [ ] Required field validation works (name, area, 5 prayer times)
- [ ] Time format validation works (must be HH:MM)
- [ ] Error messages display in red
- [ ] Submit creates masjid and redirects to list
- [ ] Cancel button returns to list
- [ ] Loading state shows during submission

#### Masjid Detail Page (`/masjids/[id]`)
- [ ] Prayer times display in color-coded cards
- [ ] Each prayer has correct color (Fajr=blue, Dhuhr=orange, etc.)
- [ ] Prayer time text is readable
- [ ] "Edit" button is visible and clickable
- [ ] "Add Task" button is orange and visible
- [ ] Masjid information displays correctly
- [ ] Associated tasks list shows tasks

#### Masjid Edit Page (`/masjids/[id]/edit`)
- [ ] Form pre-populates with existing data
- [ ] All fields editable with visible text
- [ ] Same validation as creation
- [ ] Update saves changes and redirects to detail
- [ ] Cancel returns without saving

---

### 7.3 Theme Compliance Tests

**Visual Inspection Checklist**:

#### General Theme
- [ ] All pages have dark background (`bg-salaat-black-soft`)
- [ ] All text is white/light on dark backgrounds
- [ ] No "invisible text" issues in inputs
- [ ] Orange accent color used for buttons and highlights
- [ ] Consistent spacing and padding

#### Input Fields
- [ ] Input background is dark (`bg-salaat-black-light`)
- [ ] Input text is white and clearly visible
- [ ] Placeholder text is light gray and visible
- [ ] Focus ring is orange
- [ ] Border is visible (gray on dark)

#### Buttons
- [ ] Primary buttons are orange with white text
- [ ] Hover states work (lighter orange)
- [ ] Active states work (darker orange)
- [ ] Disabled states show reduced opacity

#### Cards
- [ ] Dark cards have slightly lighter background than page
- [ ] Border is subtle gray
- [ ] Text inside cards is white
- [ ] Prayer time cards have correct gradient colors

#### Accessibility
- [ ] Text contrast meets WCAG AA standards
- [ ] Focus indicators visible on all interactive elements
- [ ] Keyboard navigation works
- [ ] Screen reader labels present

---

## 8. Implementation Order

**Phase II implementation must follow this sequence**:

### Step 1: Backend Database & Models (Week 1)
1. Set up Neon PostgreSQL connection
2. Create SQLModel models (Masjid, SpiritualTask, DailyHadith)
3. Configure Alembic migrations
4. Run initial migration
5. Create seed script
6. Test database connection

### Step 2: Backend API Endpoints (Week 1-2)
1. Implement Masjid CRUD endpoints
2. Implement Task CRUD endpoints (update FK to masjids)
3. Implement Hadith endpoints
4. Implement utility endpoints (areas, health)
5. Add CORS configuration
6. Test all endpoints with curl/Postman

### Step 3: Frontend Theme Setup (Week 2)
1. Configure Tailwind with custom colors
2. Create global CSS with theme classes
3. Update root layout with black background
4. Create Navbar with black/orange theme
5. Create form component library (FormInput, FormSelect, etc.)
6. Test theme on sample page

### Step 4: Frontend Masjid Pages (Week 2-3)
1. Masjid List page with area filter
2. Masjid Detail page with prayer times display
3. Masjid Creation form
4. Masjid Edit form
5. Integration with Task creation (pre-selection)
6. Test all flows

### Step 5: Testing & Refinement (Week 3)
1. Backend API tests (pytest)
2. Frontend manual testing
3. Fix text visibility issues
4. Test on different screen sizes
5. Accessibility review
6. Performance optimization

---

## 9. Success Criteria

**Phase II is complete when**:

✅ Database:
- Masjid table exists in Neon PostgreSQL
- Migrations applied successfully
- Seed data populated

✅ Backend:
- All Masjid CRUD endpoints functional
- Prayer times stored and retrieved correctly
- Area filtering works
- Foreign key relationship Task → Masjid works
- API documentation accessible at `/docs`

✅ Frontend:
- Black/orange/white theme applied globally
- All text clearly visible (no "invisible text" bugs)
- Input fields show white text on dark background
- Masjid creation form works end-to-end
- Masjid editing works
- Prayer times display in color-coded cards
- Task creation pre-selects masjid from URL parameter
- Area filter dropdown functional
- Mobile responsive

✅ Documentation:
- This refined specification complete
- Plan updated (via `/sp.plan`)
- Tasks created (via `/sp.tasks`)
- README with setup instructions

---

## 10. References

- **Original Phase II Spec**: `/specs/phase2-webapp.md`
- **Phase I Spec**: `/specs/phase1-cli.md`
- **Constitution**: `/specs/constitution.md`
- **Neon Documentation**: https://neon.tech/docs
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Next.js Documentation**: https://nextjs.org/docs
- **Tailwind CSS Documentation**: https://tailwindcss.com/docs

---

## 11. Next Steps

**After this specification is approved**:

1. Run `/sp.plan` to generate detailed implementation plan
2. Run `/sp.tasks` to break plan into actionable tasks
3. Run `/sp.implement` to execute tasks programmatically

**DO NOT**:
- ❌ Write code manually
- ❌ Skip the plan/tasks steps
- ❌ Modify the existing project structure without planning

**Critical Reminder**:
All implementation must flow through Claude Code's `/sp` workflow:
- `/sp.specify` (this document - DONE ✅)
- `/sp.plan` (generate implementation plan - NEXT)
- `/sp.tasks` (break into tasks - AFTER PLAN)
- `/sp.implement` (execute - AFTER TASKS)

---

**Specification Status**: ✅ Ready for Planning
**Version**: 2.0 (Refined with Masjid Backend + Theme)
**Date**: 2025-12-28
**Next Command**: `/sp.plan`
