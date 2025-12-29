# Phase II Specification – SalaatFlow Full-Stack Web Application

**Project**: SalaatFlow – Intelligent Prayer & Masjid Todo Assistant
**Phase**: II – Full-Stack Web Application
**Version**: 1.0
**Date**: 2025-12-27
**Status**: Ready for Implementation

---

## 1. Phase II Constitution – Full-Stack Evolution

### 1.1 Purpose
Phase II transforms the console application into a modern full-stack web application with persistent storage, RESTful API, and responsive web interface. This phase introduces database persistence, advanced filtering/sorting, and masjid/area management.

### 1.2 Scope
**In Scope:**
- Persistent database storage (PostgreSQL via Neon)
- RESTful API backend (FastAPI)
- Modern web frontend (Next.js 14+ with App Router)
- All Phase I features via web UI
- Intermediate Todo features: priorities, tags, search, filter, sort
- Masjid and area management
- Daily Hadith display
- Basic recurrence support (daily/weekly/monthly)

**Out of Scope:**
- AI chatbot (Phase III)
- Natural language processing
- Kubernetes deployment (Phase IV)
- Cloud deployment (Phase V)
- Advanced recurring task logic (Phase III)
- Smart reminders and notifications (Phase III)
- User authentication (optional for Phase II, required for Phase III+)

### 1.3 Domain Evolution from Phase I

| Phase I (Console) | Phase II (Web App) |
|-------------------|-------------------|
| In-memory list | PostgreSQL database |
| Dict-based tasks | SQLModel ORM models |
| CLI commands | REST API endpoints |
| Console output | React components |
| Free-text masjid/area | Normalized Masjid table with FK |
| No tags | Tag array support |
| No priorities | High/Medium/Low priorities |
| No search/sort | Full search, filter, sort UI |

### 1.4 Tech Stack

**Backend:**
- Python 3.11+
- FastAPI 0.100+
- SQLModel 0.0.14+ (SQLAlchemy + Pydantic)
- Neon PostgreSQL (serverless Postgres)
- Uvicorn (ASGI server)

**Frontend:**
- Next.js 14+ (App Router, TypeScript)
- React 18+
- TailwindCSS for styling
- Axios or Fetch for API calls
- React Query (optional, recommended for state management)

**Database:**
- PostgreSQL 15+ (via Neon)
- SQLModel for ORM

---

## 2. Data Models (SQLModel)

### 2.1 SpiritualTask Model

**Table Name**: `spiritual_tasks`

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

    # Masjid Association
    masjid_id: Optional[int] = Field(default=None, foreign_key="masjids.id")
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

**Field Descriptions:**
- `id`: Auto-incrementing primary key
- `title`: Task name (required, max 200 chars, indexed for search)
- `description`: Optional detailed description (max 2000 chars)
- `category`: Islamic practice type (Farz/Sunnah/Nafl/Deed/Other)
- `priority`: Task urgency (High/Medium/Low, indexed for filtering)
- `tags`: JSON array of tag strings (e.g., `["Quran", "Morning"]`)
- `masjid_id`: Foreign key to Masjid table (optional)
- `due_datetime`: Optional deadline or prayer time
- `recurrence`: Recurrence pattern (None/Daily/Weekly/Monthly)
- `completed`: Completion status (indexed for filtering)
- `created_at`: Creation timestamp (UTC)
- `updated_at`: Last modification timestamp (UTC)

**Priority-Category Mapping:**
- Farz → Typically High priority
- Sunnah → Typically Medium priority
- Nafl/Deed → Typically Low to Medium priority
- User can override priority for any category

---

### 2.2 Masjid Model

**Table Name**: `masjids`

```python
class Masjid(SQLModel, table=True):
    __tablename__ = "masjids"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Identity
    name: str = Field(max_length=200, index=True)
    area_name: str = Field(max_length=100, index=True)
    address: Optional[str] = Field(default=None, max_length=500)

    # Location (optional for Phase II, can be used in Phase III+)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)

    # Prayer Times (stored as time strings HH:MM)
    fajr_time: str = Field(max_length=5)  # e.g., "05:30"
    dhuhr_time: str = Field(max_length=5)  # e.g., "13:00"
    asr_time: str = Field(max_length=5)    # e.g., "16:30"
    maghrib_time: str = Field(max_length=5) # e.g., "18:15"
    isha_time: str = Field(max_length=5)   # e.g., "19:45"
    jummah_time: Optional[str] = Field(default=None, max_length=5)  # e.g., "13:30"

    # Relationships
    tasks: List["SpiritualTask"] = Relationship(back_populates="masjid")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Field Descriptions:**
- `id`: Auto-incrementing primary key
- `name`: Masjid name (required, indexed)
- `area_name`: Locality/neighborhood (required, indexed for filtering)
- `address`: Full street address (optional)
- `latitude/longitude`: GPS coordinates (optional, for future map features)
- `fajr_time` through `isha_time`: Five daily prayer times in HH:MM format
- `jummah_time`: Friday Jummah prayer time (optional)
- `tasks`: Relationship to associated SpiritualTask records

**Notes:**
- Prayer times are stored as strings for simplicity in Phase II
- Future phases can implement dynamic prayer time calculation based on location
- Area name allows filtering masjids by locality

---

### 2.3 DailyHadith Model

**Table Name**: `daily_hadiths`

```python
class DailyHadith(SQLModel, table=True):
    __tablename__ = "daily_hadiths"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Content
    content: str = Field(max_length=2000)
    reference: str = Field(max_length=200)  # e.g., "Sahih Bukhari 1234"
    language: str = Field(default="en", max_length=5)  # ISO code: en, ur, ar

    # Scheduling
    display_date: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Field Descriptions:**
- `id`: Auto-incrementing primary key
- `content`: Hadith text (max 2000 chars)
- `reference`: Source citation (e.g., "Sahih Bukhari 1234")
- `language`: Language code (en=English, ur=Urdu, ar=Arabic)
- `display_date`: Date when this hadith should be shown (indexed)
- `created_at`: Record creation timestamp

**Usage:**
- One hadith per day
- Frontend fetches hadith for `display_date = today`
- Admin can pre-populate hadiths for upcoming days

---

## 3. API Specification (FastAPI)

### 3.1 Base URL & Configuration

**Base URL**: `http://localhost:8000/api/v1`

**CORS Configuration**:
- Allow origins: `http://localhost:3000` (Next.js dev server)
- Allow methods: GET, POST, PUT, PATCH, DELETE
- Allow headers: Content-Type, Authorization

**Response Format**:
All responses use JSON with standard HTTP status codes.

---

### 3.2 Spiritual Task Endpoints

#### 3.2.1 List Tasks (with filters)

**Endpoint**: `GET /api/v1/tasks`

**Query Parameters**:
- `status` (optional): `all` | `pending` | `completed` (default: `all`)
- `category` (optional): `Farz` | `Sunnah` | `Nafl` | `Deed` | `Other`
- `priority` (optional): `High` | `Medium` | `Low`
- `masjid_id` (optional): integer
- `area_name` (optional): string
- `search` (optional): string (searches title and description)
- `sort_by` (optional): `title` | `due_date` | `priority` | `created_at` (default: `created_at`)
- `sort_order` (optional): `asc` | `desc` (default: `desc`)
- `limit` (optional): integer (default: 100, max: 500)
- `offset` (optional): integer (default: 0)

**Response**: `200 OK`
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Attend Fajr at Masjid Al-Huda",
      "description": "Wake up 30 minutes early",
      "category": "Farz",
      "priority": "High",
      "tags": ["Masjid Al-Huda", "Morning"],
      "masjid_id": 1,
      "masjid": {
        "id": 1,
        "name": "Masjid Al-Huda",
        "area_name": "DHA Phase 5"
      },
      "due_datetime": "2025-12-28T05:30:00Z",
      "recurrence": "Daily",
      "completed": false,
      "created_at": "2025-12-27T10:00:00Z",
      "updated_at": "2025-12-27T10:00:00Z"
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0
}
```

---

#### 3.2.2 Get Single Task

**Endpoint**: `GET /api/v1/tasks/{task_id}`

**Path Parameters**:
- `task_id`: integer (required)

**Response**: `200 OK`
```json
{
  "id": 1,
  "title": "Attend Fajr at Masjid Al-Huda",
  "description": "Wake up 30 minutes early",
  "category": "Farz",
  "priority": "High",
  "tags": ["Masjid Al-Huda", "Morning"],
  "masjid_id": 1,
  "masjid": {
    "id": 1,
    "name": "Masjid Al-Huda",
    "area_name": "DHA Phase 5",
    "fajr_time": "05:30"
  },
  "due_datetime": "2025-12-28T05:30:00Z",
  "recurrence": "Daily",
  "completed": false,
  "created_at": "2025-12-27T10:00:00Z",
  "updated_at": "2025-12-27T10:00:00Z"
}
```

**Error Response**: `404 Not Found`
```json
{
  "detail": "Task with ID 1 not found"
}
```

---

#### 3.2.3 Create Task

**Endpoint**: `POST /api/v1/tasks`

**Request Body**:
```json
{
  "title": "Read Surah Yaseen",
  "description": "After Fajr prayer",
  "category": "Sunnah",
  "priority": "Medium",
  "tags": ["Quran", "Morning"],
  "masjid_id": null,
  "due_datetime": "2025-12-28T06:00:00Z",
  "recurrence": "Daily"
}
```

**Validation Rules**:
- `title`: Required, 1-200 characters
- `description`: Optional, max 2000 characters
- `category`: Required, must be valid enum value
- `priority`: Optional (defaults to Medium)
- `tags`: Optional, array of strings
- `masjid_id`: Optional, must reference existing Masjid
- `due_datetime`: Optional, ISO 8601 format
- `recurrence`: Optional (defaults to None)

**Response**: `201 Created`
```json
{
  "id": 2,
  "title": "Read Surah Yaseen",
  "description": "After Fajr prayer",
  "category": "Sunnah",
  "priority": "Medium",
  "tags": ["Quran", "Morning"],
  "masjid_id": null,
  "masjid": null,
  "due_datetime": "2025-12-28T06:00:00Z",
  "recurrence": "Daily",
  "completed": false,
  "created_at": "2025-12-27T10:15:00Z",
  "updated_at": "2025-12-27T10:15:00Z"
}
```

**Error Response**: `422 Unprocessable Entity`
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

#### 3.2.4 Update Task

**Endpoint**: `PUT /api/v1/tasks/{task_id}`

**Request Body**: (all fields optional, only provided fields updated)
```json
{
  "title": "Read Surah Yaseen after Fajr",
  "priority": "High"
}
```

**Response**: `200 OK` (returns updated task, same format as Create)

**Notes**:
- `updated_at` automatically set to current timestamp
- Partial updates supported (only send changed fields)

---

#### 3.2.5 Delete Task

**Endpoint**: `DELETE /api/v1/tasks/{task_id}`

**Response**: `204 No Content`

**Error Response**: `404 Not Found`

---

#### 3.2.6 Toggle Task Completion

**Endpoint**: `PATCH /api/v1/tasks/{task_id}/toggle`

**Request Body**: (empty)

**Response**: `200 OK`
```json
{
  "id": 1,
  "completed": true,
  "updated_at": "2025-12-27T11:00:00Z"
}
```

**Notes**:
- Toggles `completed` from `false` to `true` or vice versa
- Updates `updated_at` timestamp

---

### 3.3 Masjid Endpoints

#### 3.3.1 List Masjids

**Endpoint**: `GET /api/v1/masjids`

**Query Parameters**:
- `area_name` (optional): Filter by area
- `search` (optional): Search by name or area

**Response**: `200 OK`
```json
{
  "masjids": [
    {
      "id": 1,
      "name": "Masjid Al-Huda",
      "area_name": "DHA Phase 5",
      "address": "123 Main St, DHA Phase 5, Karachi",
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
  ],
  "total": 1
}
```

---

#### 3.3.2 Get Single Masjid

**Endpoint**: `GET /api/v1/masjids/{masjid_id}`

**Response**: `200 OK` (same format as list item)

---

#### 3.3.3 Create Masjid (Admin)

**Endpoint**: `POST /api/v1/masjids`

**Request Body**:
```json
{
  "name": "Masjid Al-Noor",
  "area_name": "Gulshan-e-Iqbal",
  "address": "456 Block 13, Gulshan-e-Iqbal, Karachi",
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
- `name`: Required, 1-200 characters
- `area_name`: Required, 1-100 characters
- `address`: Optional, max 500 characters
- `latitude/longitude`: Optional, valid coordinates
- `fajr_time` through `isha_time`: Required, HH:MM format
- `jummah_time`: Optional, HH:MM format

**Response**: `201 Created` (returns created masjid)

---

#### 3.3.4 Update Masjid (Admin)

**Endpoint**: `PUT /api/v1/masjids/{masjid_id}`

**Request Body**: (same as Create, all fields optional)

**Response**: `200 OK`

---

#### 3.3.5 Delete Masjid (Admin)

**Endpoint**: `DELETE /api/v1/masjids/{masjid_id}`

**Response**: `204 No Content`

**Notes**:
- Should check if any tasks reference this masjid
- Either cascade delete or prevent deletion if tasks exist

---

### 3.4 Daily Hadith Endpoints

#### 3.4.1 Get Today's Hadith

**Endpoint**: `GET /api/v1/hadith/today`

**Query Parameters**:
- `language` (optional): `en` | `ur` | `ar` (default: `en`)

**Response**: `200 OK`
```json
{
  "id": 1,
  "content": "The best of people are those who are most beneficial to people.",
  "reference": "Sahih al-Jami 3289",
  "language": "en",
  "display_date": "2025-12-27T00:00:00Z",
  "created_at": "2025-12-27T00:00:00Z"
}
```

**Error Response**: `404 Not Found` (if no hadith for today)
```json
{
  "detail": "No hadith available for today"
}
```

---

#### 3.4.2 List All Hadiths (Admin)

**Endpoint**: `GET /api/v1/hadiths`

**Response**: `200 OK` (array of hadiths)

---

#### 3.4.3 Create Hadith (Admin)

**Endpoint**: `POST /api/v1/hadiths`

**Request Body**:
```json
{
  "content": "The best of people are those who are most beneficial to people.",
  "reference": "Sahih al-Jami 3289",
  "language": "en",
  "display_date": "2025-12-28T00:00:00Z"
}
```

**Response**: `201 Created`

---

### 3.5 Utility Endpoints

#### 3.5.1 Health Check

**Endpoint**: `GET /api/v1/health`

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-27T10:00:00Z"
}
```

---

#### 3.5.2 Get Areas List

**Endpoint**: `GET /api/v1/areas`

**Description**: Returns unique list of area names from Masjid table

**Response**: `200 OK`
```json
{
  "areas": [
    "DHA Phase 5",
    "Gulshan-e-Iqbal",
    "Clifton",
    "Malir"
  ]
}
```

---

## 4. Frontend Specification (Next.js)

### 4.1 Application Structure

```
frontend/
├── app/
│   ├── layout.tsx                 # Root layout with navbar
│   ├── page.tsx                   # Dashboard (home page)
│   ├── tasks/
│   │   ├── page.tsx              # Task list view
│   │   ├── new/page.tsx          # Create task form
│   │   └── [id]/
│   │       ├── page.tsx          # Task detail view
│   │       └── edit/page.tsx     # Edit task form
│   ├── masjids/
│   │   ├── page.tsx              # Masjid list view
│   │   └── [id]/page.tsx         # Masjid detail view
│   └── api/                       # (Optional) API route handlers
├── components/
│   ├── TaskCard.tsx              # Individual task display
│   ├── TaskForm.tsx              # Task create/edit form
│   ├── TaskList.tsx              # Task list with filters
│   ├── TaskFilters.tsx           # Filter/sort controls
│   ├── MasjidCard.tsx            # Masjid display card
│   ├── MasjidSelector.tsx        # Area/masjid selector
│   ├── DailyHadithBox.tsx        # Hadith display component
│   ├── Navbar.tsx                # Top navigation bar
│   └── PriorityBadge.tsx         # Priority indicator
├── lib/
│   ├── api.ts                    # API client functions
│   ├── types.ts                  # TypeScript interfaces
│   └── utils.ts                  # Helper functions
└── public/
    └── ...                        # Static assets
```

---

### 4.2 Pages & Routes

#### 4.2.1 Dashboard (Home Page)

**Route**: `/`

**Components**:
- `DailyHadithBox`: Displays today's hadith
- `TaskList`: Shows recent/upcoming tasks (max 5-10)
- `MasjidSelector`: Dropdown to select area, shows masjid count
- Quick stats: Total tasks, Completed today, Pending

**Layout**:
```
┌─────────────────────────────────────────┐
│ Navbar: [Logo] [Tasks] [Masjids] [+]   │
├─────────────────────────────────────────┤
│ Dashboard                               │
├──────────────┬──────────────────────────┤
│ Daily Hadith │ Upcoming Tasks           │
│ [Hadith box] │ - [ ] Attend Fajr        │
│              │ - [ ] Read Quran         │
│              │ [View All Tasks →]       │
├──────────────┴──────────────────────────┤
│ Masjids in Your Area                    │
│ Area: [DHA Phase 5 ▼]                   │
│ [Masjid Al-Huda] [Masjid Al-Noor]       │
└─────────────────────────────────────────┘
```

---

#### 4.2.2 Task List Page

**Route**: `/tasks`

**Components**:
- `TaskFilters`: Status, Category, Priority, Masjid, Search, Sort
- `TaskList`: Paginated task list
- `TaskCard`: Individual task display

**Features**:
- Search by title/description
- Filter by: status (all/pending/completed), category, priority, masjid, area
- Sort by: due date, priority, title, created date
- Click task to view details
- Quick complete toggle (checkbox)
- Edit/Delete buttons

**Layout**:
```
┌─────────────────────────────────────────┐
│ Tasks                          [+ New]  │
├─────────────────────────────────────────┤
│ Filters:                                │
│ [Search...] [Status▼] [Category▼]      │
│ [Priority▼] [Masjid▼] [Sort by▼]       │
├─────────────────────────────────────────┤
│ ☐ Attend Fajr at Masjid Al-Huda        │
│   Farz | High | Due: Tomorrow 5:30 AM  │
│   [Edit] [Delete]                       │
├─────────────────────────────────────────┤
│ ☑ Read Surah Yaseen                     │
│   Sunnah | Medium | Completed           │
│   [Edit] [Delete]                       │
├─────────────────────────────────────────┤
│ [< Prev] Page 1 of 3 [Next >]          │
└─────────────────────────────────────────┘
```

---

#### 4.2.3 Task Create/Edit Form

**Routes**:
- Create: `/tasks/new`
- Create with pre-selected masjid: `/tasks/new?masjid={id}`
- Edit: `/tasks/[id]/edit`

**Form Fields**:
- Title (required, text input)
- Description (optional, textarea)
- Category (required, dropdown: Farz/Sunnah/Nafl/Deed/Other)
- Priority (dropdown: High/Medium/Low)
- Tags (multi-input or comma-separated)
- Masjid (dropdown with area filter)
  - **Pre-selection feature**: If URL contains `?masjid={id}`, automatically selects that masjid
  - Allows user to change selection if needed
- Due Date/Time (datetime-local input)
- Recurrence (dropdown: None/Daily/Weekly/Monthly)

**Buttons**:
- Save
- Cancel (returns to task list)

**Validation**:
- Client-side: Required fields, max lengths
- Server-side: API validation errors displayed

**Query Parameters**:
- `masjid`: Optional integer - Pre-selects masjid in form (used when creating task from masjid detail page)

---

#### 4.2.4 Task Detail Page

**Route**: `/tasks/[id]`

**Display**:
- All task fields in read-only format
- Masjid details if associated (name, area, prayer times)
- Created/Updated timestamps
- Action buttons: Edit, Delete, Toggle Complete

---

#### 4.2.5 Masjid List Page

**Route**: `/masjids`

**Components**:
- Area filter dropdown
- `MasjidCard`: Shows masjid name, area, prayer times

**Layout**:
```
┌─────────────────────────────────────────┐
│ Masjids                        [+ New]  │
├─────────────────────────────────────────┤
│ Filter by Area: [All Areas ▼]          │
├─────────────────────────────────────────┤
│ Masjid Al-Huda                          │
│ DHA Phase 5                             │
│ Fajr: 5:30 | Dhuhr: 1:00 | Asr: 4:30   │
│ Maghrib: 6:15 | Isha: 7:45              │
│ [View Details]                          │
├─────────────────────────────────────────┤
│ Masjid Al-Noor                          │
│ Gulshan-e-Iqbal                         │
│ ...                                     │
└─────────────────────────────────────────┘
```

---

#### 4.2.6 Masjid Detail Page

**Route**: `/masjids/[id]`

**Display**:
- Full masjid information
- Address, coordinates (if available)
- **Prayer Times Display**: Color-coded grid showing all 5 daily prayers (Fajr, Dhuhr, Asr, Maghrib, Isha) plus Jummah time
  - Each prayer time in its own colored card
  - Visually distinct colors for each prayer
  - Responsive grid layout (2 columns on mobile, 3 on tablet, 5 on desktop)
- Tasks associated with this masjid
- **Add Task Button**: Creates new task with masjid pre-selected
  - Button redirects to `/tasks/new?masjid={id}`
  - Task form automatically populates masjid field
- Show/hide completed tasks toggle
- **Edit Button**: Navigates to `/masjids/[id]/edit` for updating masjid information
- Delete button (admin only - future feature)

---

#### 4.2.7 Masjid Creation Page

**Route**: `/masjids/new`

**Purpose**: Create new masjid with complete information and prayer times

**Form Sections**:

1. **Basic Information**:
   - Masjid Name (required) - Text input
   - Area (required) - Text input
   - City (optional) - Text input
   - Address (optional) - Textarea
   - Imam Name (optional) - Text input
   - Phone (optional) - Tel input

2. **Prayer Times** (24-hour HH:MM format):
   - Fajr (required) - Time input
   - Dhuhr (required) - Time input
   - Asr (required) - Time input
   - Maghrib (required) - Time input
   - Isha (required) - Time input
   - Jummah (optional) - Time input

**Validation Rules**:
- Name: Required, non-empty string
- Area: Required, non-empty string
- Prayer times: Must match regex `^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$`
- All 5 daily prayers required; Jummah optional
- Inline error messages for invalid fields

**Actions**:
- **Save Masjid**: Submits form, creates masjid, redirects to `/masjids`
- **Cancel**: Returns to `/masjids` without saving

**User Experience**:
- Loading state during submission
- Error messages displayed at top if API fails
- Success redirect to masjids list

---

#### 4.2.8 Masjid Edit Page

**Route**: `/masjids/[id]/edit`

**Purpose**: Update existing masjid information and prayer times

**Features**:
- Same form fields as creation page
- Form pre-populated with existing masjid data
- Same validation rules as creation
- Loading state while fetching masjid data
- 404 handling if masjid not found

**Actions**:
- **Update Masjid**: Submits changes, redirects to `/masjids/[id]`
- **Cancel**: Returns to `/masjids/[id]` without saving

**User Flow**:
```
Masjid Detail → Click "Edit" →
Edit Form (Pre-filled) → Modify Fields →
Click "Update" → Success → Return to Detail Page
```

---

### 4.3 Components Specification

#### 4.3.1 TaskCard Component

**Props**:
```typescript
interface TaskCardProps {
  task: Task;
  onToggleComplete: (taskId: number) => void;
  onEdit: (taskId: number) => void;
  onDelete: (taskId: number) => void;
}
```

**Features**:
- Checkbox for completion toggle
- Priority badge (color-coded: High=red, Medium=yellow, Low=green)
- Category badge
- Due date display (with "overdue" warning if past)
- Tags as small pills
- Edit/Delete action buttons

---

#### 4.3.2 TaskFilters Component

**Props**:
```typescript
interface TaskFiltersProps {
  filters: TaskFilters;
  onFilterChange: (filters: TaskFilters) => void;
  masjids: Masjid[];
}

interface TaskFilters {
  status: 'all' | 'pending' | 'completed';
  category?: string;
  priority?: string;
  masjidId?: number;
  search?: string;
  sortBy: string;
  sortOrder: 'asc' | 'desc';
}
```

**Features**:
- Search input (debounced)
- Dropdown filters (status, category, priority, masjid)
- Sort controls (field + direction)
- Clear filters button

---

#### 4.3.3 DailyHadithBox Component

**Props**:
```typescript
interface DailyHadithBoxProps {
  language?: 'en' | 'ur' | 'ar';
}
```

**Features**:
- Fetches today's hadith on mount
- Displays content and reference
- Language selector (optional)
- Loading and error states

**Design**:
- Bordered card with subtle Islamic pattern background
- Bismillah header
- Hadith text in readable font
- Reference in smaller italic text

---

#### 4.3.4 MasjidSelector Component

**Props**:
```typescript
interface MasjidSelectorProps {
  onAreaChange: (area: string) => void;
  onMasjidSelect: (masjid: Masjid) => void;
}
```

**Features**:
- Area dropdown (populated from `/api/v1/areas`)
- Masjid list filtered by selected area
- Displays prayer times for selected masjid

---

### 4.4 TypeScript Interfaces

**File**: `lib/types.ts`

```typescript
export interface Task {
  id: number;
  title: string;
  description?: string;
  category: 'Farz' | 'Sunnah' | 'Nafl' | 'Deed' | 'Other';
  priority: 'High' | 'Medium' | 'Low';
  tags: string[];
  masjid_id?: number;
  masjid?: Masjid;
  due_datetime?: string; // ISO 8601
  recurrence: 'None' | 'Daily' | 'Weekly' | 'Monthly';
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface Masjid {
  id: number;
  name: string;
  area_name: string;
  address?: string;
  latitude?: number;
  longitude?: number;
  fajr_time: string;
  dhuhr_time: string;
  asr_time: string;
  maghrib_time: string;
  isha_time: string;
  jummah_time?: string;
  created_at: string;
  updated_at: string;
}

export interface DailyHadith {
  id: number;
  content: string;
  reference: string;
  language: string;
  display_date: string;
  created_at: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}
```

---

### 4.5 API Client

**File**: `lib/api.ts`

```typescript
import axios from 'axios';
import { Task, Masjid, DailyHadith } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Task API
export const taskApi = {
  list: (params?: any) => api.get<{ tasks: Task[]; total: number }>('/tasks', { params }),
  get: (id: number) => api.get<Task>(`/tasks/${id}`),
  create: (data: Partial<Task>) => api.post<Task>('/tasks', data),
  update: (id: number, data: Partial<Task>) => api.put<Task>(`/tasks/${id}`, data),
  delete: (id: number) => api.delete(`/tasks/${id}`),
  toggle: (id: number) => api.patch<Task>(`/tasks/${id}/toggle`),
};

// Masjid API
export const masjidApi = {
  list: (params?: any) => api.get<{ masjids: Masjid[]; total: number }>('/masjids', { params }),
  get: (id: number) => api.get<Masjid>(`/masjids/${id}`),
  create: (data: Partial<Masjid>) => api.post<Masjid>('/masjids', data),
  update: (id: number, data: Partial<Masjid>) => api.put<Masjid>(`/masjids/${id}`, data),
  delete: (id: number) => api.delete(`/masjids/${id}`),
};

// Hadith API
export const hadithApi = {
  today: (language?: string) => api.get<DailyHadith>('/hadith/today', { params: { language } }),
};

// Utility API
export const utilityApi = {
  health: () => api.get('/health'),
  areas: () => api.get<{ areas: string[] }>('/areas'),
};
```

---

## 5. Database Schema & Setup

### 5.1 Neon PostgreSQL Setup

**Steps**:
1. Create Neon project at https://neon.tech
2. Create database: `salaatflow_db`
3. Get connection string: `postgresql://user:password@host/salaatflow_db`
4. Store in environment variable: `DATABASE_URL`

**Environment Variables** (`.env`):
```env
# Backend
DATABASE_URL=postgresql://user:password@host/salaatflow_db
CORS_ORIGINS=http://localhost:3000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

### 5.2 Database Migrations

**Using Alembic** (SQLAlchemy migration tool):

**Initial Migration**:
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

**Migration Script** (auto-generated):
- Creates `spiritual_tasks` table
- Creates `masjids` table
- Creates `daily_hadiths` table
- Adds foreign key constraint: `spiritual_tasks.masjid_id` → `masjids.id`
- Creates indexes on commonly queried fields

---

### 5.3 Seed Data

**Seed Script**: `backend/seed.py`

**Sample Data**:
- 5-10 masjids across different areas (DHA Phase 5, Gulshan-e-Iqbal, Clifton, Malir)
- 20-30 sample spiritual tasks with variety of categories, priorities, and statuses
- 7-10 daily hadiths for upcoming week

**Execution**:
```bash
python backend/seed.py
```

---

## 6. Acceptance Criteria

### 6.1 Backend API Tests

#### 6.1.1 Task CRUD Operations
- [ ] Create task with all fields returns 201 with task ID
- [ ] Create task with missing title returns 422 validation error
- [ ] List tasks without filters returns all tasks
- [ ] List tasks with `status=pending` returns only incomplete tasks
- [ ] List tasks with `category=Farz` returns only Farz tasks
- [ ] List tasks with `search=Fajr` returns tasks containing "Fajr"
- [ ] List tasks with `sort_by=due_date&sort_order=asc` returns sorted results
- [ ] Get single task by ID returns 200 with task details
- [ ] Get non-existent task returns 404
- [ ] Update task modifies fields and updates `updated_at`
- [ ] Delete task returns 204 and removes from database
- [ ] Toggle task completion flips `completed` status

#### 6.1.2 Masjid Operations
- [ ] Create masjid with valid prayer times returns 201
- [ ] List masjids with `area_name` filter returns only matching masjids
- [ ] Get single masjid returns all prayer times
- [ ] Update masjid prayer times persists changes

#### 6.1.3 Hadith Operations
- [ ] Get today's hadith returns hadith for current date
- [ ] Get today's hadith with no entry returns 404

---

### 6.2 Frontend UI Tests

#### 6.2.1 Dashboard
- [ ] Dashboard displays daily hadith
- [ ] Dashboard shows upcoming tasks (max 10)
- [ ] Area selector populates from API
- [ ] Selecting area filters masjid display

#### 6.2.2 Task Management
- [ ] Create task form validates required fields
- [ ] Create task form submits and redirects to task list
- [ ] Task list displays tasks with correct status icons
- [ ] Clicking checkbox toggles task completion
- [ ] Search box filters tasks client-side or server-side
- [ ] Category filter dropdown updates task list
- [ ] Sort by due date arranges tasks chronologically
- [ ] Edit task form pre-populates with current values
- [ ] Delete task shows confirmation dialog
- [ ] Delete task removes from list after confirmation

#### 6.2.3 Masjid Management
- [ ] Masjid list displays all masjids
- [ ] Area filter reduces masjid list to selected area
- [ ] Masjid detail page shows all 5 prayer times
- [ ] Tasks associated with masjid appear in detail view

---

### 6.3 Integration Tests

#### 6.3.1 End-to-End Workflows

**Test 1: Create Task Linked to Masjid**
1. Navigate to `/tasks/new`
2. Fill in: Title="Attend Jummah", Category="Farz", Priority="High"
3. Select masjid: "Masjid Al-Huda" (auto-populates area)
4. Set due_datetime to next Friday 1:30 PM
5. Submit form
6. Verify redirect to task list
7. Verify new task appears with masjid name
8. Click task to view details
9. Verify masjid prayer times displayed

**Expected**: Task created successfully, masjid association works, prayer times visible

**Test 2: Filter Tasks by Area via Masjid**
1. Navigate to `/tasks`
2. Apply masjid filter: Select "Masjid Al-Huda"
3. Verify only tasks linked to that masjid appear
4. Clear filter
5. Verify all tasks appear again

**Expected**: Filtering works correctly, clear filter resets

**Test 3: Complete Task and Filter**
1. Navigate to `/tasks`
2. Click checkbox next to pending task
3. Verify task status changes to completed (checkmark)
4. Apply filter: "Completed"
5. Verify completed task appears
6. Apply filter: "Pending"
7. Verify completed task does NOT appear

**Expected**: Completion toggle and filtering work together

**Test 4: Search Tasks**
1. Navigate to `/tasks`
2. Enter "Fajr" in search box
3. Verify only tasks with "Fajr" in title or description appear
4. Clear search
5. Verify all tasks return

**Expected**: Search filters correctly

**Test 5: Sort Tasks by Priority**
1. Navigate to `/tasks`
2. Select "Sort by: Priority"
3. Verify High priority tasks appear first
4. Change to descending order
5. Verify Low priority tasks appear first

**Expected**: Sorting works correctly

---

## 7. Technical Requirements

### 7.1 Backend Requirements

**Dependencies** (`requirements.txt`):
```
fastapi==0.110.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
alembic==1.13.1
python-dotenv==1.0.0
pydantic==2.5.0
```

**File Structure**:
```
backend/
├── main.py                 # FastAPI app entry point
├── models.py               # SQLModel models
├── database.py             # Database connection
├── routers/
│   ├── tasks.py           # Task endpoints
│   ├── masjids.py         # Masjid endpoints
│   └── hadiths.py         # Hadith endpoints
├── schemas.py              # Pydantic request/response schemas
├── crud.py                 # Database operations
├── seed.py                 # Seed data script
├── alembic/                # Migration scripts
├── .env                    # Environment variables
└── requirements.txt
```

---

### 7.2 Frontend Requirements

**Dependencies** (`package.json`):
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "axios": "^1.6.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0"
  }
}
```

**Next.js Configuration** (`next.config.js`):
```javascript
module.exports = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  },
};
```

---

### 7.3 Development Environment

**Backend Server**:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend Server**:
```bash
cd frontend
npm run dev
# Runs on http://localhost:3000
```

**Database**:
- Neon PostgreSQL (cloud-hosted)
- Connection via `DATABASE_URL` environment variable

---

## 8. Deployment Considerations (Not Required for Phase II)

**Future Deployment** (Phase IV-V):
- Backend: Docker container → Kubernetes
- Frontend: Vercel or Docker container → Kubernetes
- Database: Neon (already cloud-hosted)

**For Phase II**:
- Development environment only (localhost)
- No production deployment required

---

## 9. Non-Functional Requirements

### 9.1 Performance
- API response time: < 200ms for simple queries
- Frontend page load: < 2s on 3G connection
- Database queries optimized with indexes

### 9.2 Security
- CORS properly configured
- SQL injection prevention (via SQLModel ORM)
- Input validation on both client and server
- (Optional) API authentication with JWT

### 9.3 Usability
- Mobile-responsive design (Tailwind breakpoints)
- Accessible forms (proper labels, ARIA attributes)
- Clear error messages
- Loading states for async operations

### 9.4 Code Quality
- Backend: Type hints, docstrings, FastAPI auto-docs
- Frontend: TypeScript strict mode, ESLint
- Consistent naming conventions
- Component reusability

---

## 10. Testing Strategy

### 10.1 Backend Testing
- Unit tests: CRUD functions (pytest)
- Integration tests: API endpoints (FastAPI TestClient)
- Database tests: SQLModel operations

### 10.2 Frontend Testing
- Component tests: Jest + React Testing Library
- E2E tests: Playwright or Cypress (optional)
- Manual testing: All user workflows

### 10.3 Test Coverage Goals
- Backend: > 80% line coverage
- Frontend: > 60% component coverage
- All acceptance criteria tested

---

## 11. Documentation Requirements

### 11.1 API Documentation
- FastAPI auto-generated docs at `/docs` (Swagger UI)
- `/redoc` alternative documentation

### 11.2 Frontend Documentation
- Component props documentation (TSDoc)
- README with setup instructions
- Environment variables guide

### 11.3 User Documentation
- Phase II README with:
  - Installation steps
  - Running instructions
  - Feature walkthrough
  - Screenshots

---

## 12. Migration from Phase I

### 12.1 Data Migration
- No automatic migration (Phase I was in-memory)
- Users start fresh in Phase II
- Seed script provides sample data

### 12.2 Feature Parity
All Phase I features must work in Phase II:
- [x] Add spiritual task
- [x] View task list
- [x] Edit task
- [x] Delete task
- [x] Complete/uncomplete task
- [x] Filter by status (pending/completed)
- [x] Islamic categories (Farz/Sunnah/Nafl/Deed)

### 12.3 New Features in Phase II
- [ ] Persistent storage (database)
- [ ] Web UI instead of CLI
- [ ] Priorities (High/Medium/Low)
- [ ] Tags support
- [ ] Advanced filtering (category, priority, masjid, search)
- [ ] Sorting (multiple fields)
- [ ] Masjid management with prayer times
- [ ] Daily Hadith display
- [ ] Basic recurrence support

---

## 13. Future Phase III Preview

Phase III will add:
- AI chatbot (OpenAI ChatKit + Agents SDK)
- Natural language task management
- Intelligent prayer time reminders
- Advanced recurring task logic
- MCP SDK integrations

**Not in Scope for Phase II**

---

## References

- **Phase I Specification**: `/specs/phase1-cli.md`
- **Global Constitution**: `/specs/constitution.md`
- **Phase I Implementation**: `/phase1/`
- **Next Steps**: Generate Phase II implementation plan (`/sp.plan`)

---

**Specification Status**: ✅ Ready for Implementation Plan
**Next Command**: `/sp.plan` to generate Phase II implementation plan
**Estimated Scope**: 2-3 weeks development time (full-time equivalent)
