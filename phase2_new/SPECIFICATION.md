# SalaatFlow Phase II - Refined Full-Stack Specification

**Version**: 2.0
**Date**: December 27, 2025
**Status**: Implementation Required

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Backend Specification](#backend-specification)
4. [Frontend Specification](#frontend-specification)
5. [Integration Requirements](#integration-requirements)
6. [API Contract Specifications](#api-contract-specifications)
7. [Acceptance Criteria](#acceptance-criteria)
8. [Implementation Checklist](#implementation-checklist)

---

## Executive Summary

This refined specification ensures that **all modules**, particularly the **Tasks** and **Masjids** features, are **fully implemented with working code** and not left as empty stubs. The specification mandates a clear folder structure, complete CRUD operations, proper frontend-backend integration, and verifiable acceptance criteria.

### Key Requirements

- **Backend**: Complete FastAPI routers with all CRUD endpoints for Tasks, Masjids, and Hadith
- **Frontend**: Fully implemented Next.js pages for viewing, creating, editing, and managing Tasks and Masjids
- **Integration**: Working API client with proper error handling and loading states
- **No Empty Folders**: Every module folder must contain at least one page, component, and utility file with working code

---

## Architecture Overview

```
SalaatFlow Phase II
│
├── Backend (FastAPI + PostgreSQL)
│   ├── Database Layer (SQLModel ORM)
│   ├── Business Logic (Routers)
│   └── API Layer (RESTful endpoints)
│
├── Frontend (Next.js 14 App Router)
│   ├── Pages (Server & Client Components)
│   ├── Components (Reusable UI)
│   └── API Client (Axios)
│
└── Database (PostgreSQL on Neon)
    ├── spiritual_tasks
    ├── masjids
    └── daily_hadith
```

---

## Backend Specification

### Directory Structure (Required)

```
backend/
├── models.py                    # All SQLModel database models
├── database.py                  # Database session and connection
├── config.py                    # Environment configuration
├── main.py                      # FastAPI application entry point
├── alembic/                     # Database migrations
│   ├── versions/                # Migration files
│   └── env.py
├── routers/                     # API route handlers
│   ├── __init__.py
│   ├── tasks.py                 # ✅ MUST BE FULLY IMPLEMENTED
│   ├── masjids.py               # ✅ MUST BE FULLY IMPLEMENTED
│   └── hadith.py                # ✅ MUST BE FULLY IMPLEMENTED
├── requirements.txt             # Python dependencies
└── seed_data.py                 # Database seeding script
```

### 1. Tasks Module (`routers/tasks.py`)

**Status**: ✅ Currently implemented - Must remain complete

**Required Endpoints**:

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/v1/tasks` | List all tasks with filters | Required ✅ |
| GET | `/api/v1/tasks/{id}` | Get single task | Required ✅ |
| GET | `/api/v1/tasks/upcoming` | Get upcoming tasks | Required ✅ |
| GET | `/api/v1/tasks/stats/summary` | Get task statistics | Required ✅ |
| POST | `/api/v1/tasks` | Create new task | Required ✅ |
| PUT | `/api/v1/tasks/{id}` | Update entire task | Required ✅ |
| PATCH | `/api/v1/tasks/{id}/complete` | Mark task complete | Required ✅ |
| PATCH | `/api/v1/tasks/{id}/incomplete` | Mark task incomplete | Required ✅ |
| DELETE | `/api/v1/tasks/{id}` | Delete task | Required ✅ |
| POST | `/api/v1/tasks/bulk/complete` | Bulk complete tasks | Required ✅ |
| POST | `/api/v1/tasks/bulk/delete` | Bulk delete tasks | Required ✅ |

**Model**: `SpiritualTask`

```python
class SpiritualTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=2000)
    category: TaskCategory  # Farz, Sunnah, Nafl, Deed, Other
    priority: Priority  # Urgent, High, Medium, Low
    tags: Optional[str]  # Comma-separated tags
    masjid_id: Optional[int] = Field(foreign_key="masjids.id")
    masjid: Optional[Masjid] = Relationship(back_populates="tasks")
    due_datetime: Optional[datetime]
    recurrence: Recurrence  # None, Daily, Weekly, Monthly
    completed: bool = Field(default=False)
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```

**Query Parameters for GET /tasks**:
- `category` (TaskCategory): Filter by category
- `priority` (Priority): Filter by priority
- `completed` (bool): Filter by completion status
- `masjid_id` (int): Filter by masjid
- `recurrence` (Recurrence): Filter by recurrence
- `search` (str): Search in title and description
- `sort_by` (str): Field to sort by (default: created_at)
- `sort_order` (str): asc or desc (default: desc)
- `skip` (int): Pagination offset (default: 0)
- `limit` (int): Pagination limit (default: 100, max: 1000)

### 2. Masjids Module (`routers/masjids.py`)

**Status**: ✅ Currently implemented - Must remain complete

**Required Endpoints**:

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/v1/masjids` | List all masjids | Required ✅ |
| GET | `/api/v1/masjids/{id}` | Get single masjid | Required ✅ |
| GET | `/api/v1/masjids/{id}/tasks` | Get tasks for masjid | Required ✅ |
| POST | `/api/v1/masjids` | Create new masjid | Required ✅ |
| PUT | `/api/v1/masjids/{id}` | Update masjid | Required ✅ |
| DELETE | `/api/v1/masjids/{id}` | Delete masjid | Required ✅ |

**Model**: `Masjid`

```python
class Masjid(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200, index=True)
    area: Optional[str] = Field(max_length=200)  # Area/neighborhood name
    city: Optional[str] = Field(max_length=100)
    address: Optional[str] = Field(max_length=500)
    imam_name: Optional[str] = Field(max_length=200)
    phone: Optional[str] = Field(max_length=20)
    facilities: Optional[str]  # JSON string: parking, wudu, library, etc.
    created_at: datetime
    updated_at: datetime
    tasks: List[SpiritualTask] = Relationship(back_populates="masjid")
```

**Query Parameters for GET /masjids**:
- `city` (str): Filter by city (case-insensitive)
- `area` (str): Filter by area (case-insensitive)
- `search` (str): Search in masjid name
- `skip` (int): Pagination offset
- `limit` (int): Pagination limit

### 3. Daily Hadith Module (`routers/hadith.py`)

**Status**: ✅ Currently implemented - Must remain complete

**Required Endpoints**:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/hadith/today` | Get today's hadith |
| GET | `/api/v1/hadith` | List all hadith entries |
| GET | `/api/v1/hadith/date/{date}` | Get hadith by date (YYYY-MM-DD) |
| GET | `/api/v1/hadith/{id}` | Get hadith by ID |
| POST | `/api/v1/hadith` | Create new hadith entry |
| PUT | `/api/v1/hadith/{id}` | Update hadith |
| DELETE | `/api/v1/hadith/{id}` | Delete hadith |

**Model**: `DailyHadith`

```python
class DailyHadith(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hadith_date: date = Field(index=True, unique=True)
    arabic_text: str = Field(max_length=2000)
    english_translation: str = Field(max_length=2000)
    narrator: str = Field(max_length=200)
    source: str = Field(max_length=200)  # e.g., "Sahih Bukhari 1234"
    theme: Optional[str] = Field(max_length=100)  # e.g., "Patience", "Prayer"
    created_at: datetime
```

---

## Frontend Specification

### Directory Structure (Required)

```
frontend/
├── app/                         # Next.js App Router
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home/Dashboard page
│   ├── globals.css             # Global styles
│   │
│   ├── tasks/                  # ✅ MUST BE FULLY IMPLEMENTED (NOT EMPTY)
│   │   ├── page.tsx            # Tasks list page (REQUIRED)
│   │   ├── new/
│   │   │   └── page.tsx        # Create task page (REQUIRED)
│   │   ├── [id]/
│   │   │   ├── page.tsx        # Task detail page (REQUIRED)
│   │   │   └── edit/
│   │   │       └── page.tsx    # Edit task page (REQUIRED)
│   │   └── components/         # Task-specific components
│   │       ├── TaskList.tsx    # Task list component (REQUIRED)
│   │       ├── TaskForm.tsx    # Task form component (REQUIRED)
│   │       ├── TaskCard.tsx    # Task card component (REQUIRED)
│   │       └── TaskFilters.tsx # Filters component (REQUIRED)
│   │
│   ├── masjids/                # ✅ MUST BE FULLY IMPLEMENTED (NOT EMPTY)
│   │   ├── page.tsx            # Masjids list page (REQUIRED)
│   │   ├── [id]/
│   │   │   └── page.tsx        # Masjid detail page (REQUIRED)
│   │   └── components/         # Masjid-specific components
│   │       ├── MasjidList.tsx  # Masjid list component (REQUIRED)
│   │       ├── MasjidCard.tsx  # Masjid card component (REQUIRED)
│   │       └── AreaFilter.tsx  # Area filter component (REQUIRED)
│   │
│   └── hadith/                 # Hadith feature
│       └── page.tsx            # Daily hadith page (REQUIRED)
│
├── components/                  # Shared components
│   ├── Navbar.tsx              # ✅ Already exists
│   └── TaskCard.tsx            # ✅ Already exists (move to tasks/components/)
│
├── lib/                        # Utilities and API client
│   ├── api.ts                  # ✅ API client (already implemented)
│   ├── types.ts                # ✅ TypeScript types (already implemented)
│   └── utils.ts                # Helper functions (to be created)
│
├── public/                     # Static assets
├── next.config.js              # Next.js configuration
├── tailwind.config.ts          # Tailwind configuration
├── tsconfig.json               # TypeScript configuration
└── package.json                # Dependencies
```

### 1. Tasks Feature (Frontend)

#### **app/tasks/page.tsx** (REQUIRED - Main Tasks List)

**Purpose**: Display all tasks with filtering, sorting, and search capabilities

**Required Functionality**:
1. Fetch tasks from `/api/v1/tasks` on page load
2. Display tasks in a responsive grid/list
3. Search box for title/description search
4. Filter controls:
   - Category dropdown (Farz, Sunnah, Nafl, Deed, Other)
   - Priority dropdown (Urgent, High, Medium, Low)
   - Status filter (All, Completed, Pending)
   - Masjid filter (dropdown of masjids)
   - Area filter (if masjid selected)
5. Sort controls:
   - Sort by: Due Date, Priority, Title, Created Date
   - Sort order: Ascending, Descending
6. Actions:
   - "New Task" button → navigates to `/tasks/new`
   - Each task shows "Edit", "Complete/Incomplete", "Delete" buttons
7. Loading state (spinner)
8. Error state (error message)
9. Empty state ("No tasks found")

**Data Flow**:
```typescript
import api from '@/lib/api'
import { SpiritualTask, TaskFilters } from '@/lib/types'

// Fetch tasks with filters
const tasks = await api.getTasks({
  category: selectedCategory,
  priority: selectedPriority,
  completed: statusFilter,
  search: searchText,
  sort_by: sortBy,
  sort_order: sortOrder,
})
```

**UI Requirements**:
- Responsive design (mobile, tablet, desktop)
- Task cards with color-coded priority
- Category badges
- Due date highlighting (overdue in red)
- Quick actions (complete, delete)
- Bulk select for bulk operations

#### **app/tasks/new/page.tsx** (REQUIRED - Create Task)

**Purpose**: Form to create a new spiritual task

**Required Fields**:
1. Title (text input, required)
2. Description (textarea, optional)
3. Category (dropdown: Farz, Sunnah, Nafl, Deed, Other)
4. Priority (dropdown: Urgent, High, Medium, Low)
5. Tags (text input, comma-separated)
6. Masjid (searchable dropdown, optional)
7. Due Date & Time (datetime picker, optional)
8. Recurrence (dropdown: None, Daily, Weekly, Monthly)

**Actions**:
- "Create Task" button (submits form)
- "Cancel" button (navigates back)

**Validation**:
- Title is required
- Category must be selected
- Priority must be selected
- Due date must be in the future (if provided)

**Data Flow**:
```typescript
const newTask = await api.createTask({
  title: formData.title,
  description: formData.description,
  category: formData.category,
  priority: formData.priority,
  tags: formData.tags,
  masjid_id: formData.masjidId,
  due_datetime: formData.dueDateTime,
  recurrence: formData.recurrence,
})
// Navigate to /tasks or /tasks/{newTask.id}
```

#### **app/tasks/[id]/page.tsx** (REQUIRED - Task Detail)

**Purpose**: View detailed information about a single task

**Display**:
- Task title (large heading)
- Description (formatted text)
- Category badge
- Priority indicator
- Tags (as chips)
- Masjid name (link to masjid detail if set)
- Due date & time
- Recurrence pattern
- Completion status
- Created date
- Updated date

**Actions**:
- "Edit" button → navigates to `/tasks/{id}/edit`
- "Mark Complete/Incomplete" toggle
- "Delete" button (with confirmation)
- "Back to Tasks" link

**Data Flow**:
```typescript
const task = await api.getTask(taskId)
```

#### **app/tasks/[id]/edit/page.tsx** (REQUIRED - Edit Task)

**Purpose**: Form to edit an existing task

**Requirements**:
- Same form fields as create page
- Pre-populated with existing task data
- "Update Task" button
- "Cancel" button

**Data Flow**:
```typescript
// Load existing task
const task = await api.getTask(taskId)

// Update task
const updatedTask = await api.updateTask(taskId, formData)
```

#### **app/tasks/components/TaskList.tsx** (REQUIRED)

**Purpose**: Reusable component to display list of tasks

**Props**:
```typescript
interface TaskListProps {
  tasks: SpiritualTask[]
  onEdit: (task: SpiritualTask) => void
  onComplete: (taskId: number) => void
  onDelete: (taskId: number) => void
}
```

**Features**:
- Renders list of TaskCard components
- Handles empty state
- Supports grid or list view

#### **app/tasks/components/TaskForm.tsx** (REQUIRED)

**Purpose**: Reusable form for create/edit task

**Props**:
```typescript
interface TaskFormProps {
  initialData?: SpiritualTask | null
  onSubmit: (data: TaskFormData) => Promise<void>
  onCancel: () => void
  isLoading?: boolean
}
```

**Features**:
- All form fields
- Validation
- Loading state
- Error handling

#### **app/tasks/components/TaskCard.tsx** (REQUIRED)

**Purpose**: Display individual task in card format

**Props**:
```typescript
interface TaskCardProps {
  task: SpiritualTask
  onEdit?: (task: SpiritualTask) => void
  onComplete?: (taskId: number) => void
  onDelete?: (taskId: number) => void
}
```

**Display**:
- Title, description (truncated)
- Category badge, priority indicator
- Due date, completion status
- Quick action buttons

#### **app/tasks/components/TaskFilters.tsx** (REQUIRED)

**Purpose**: Filter controls for task list

**Props**:
```typescript
interface TaskFiltersProps {
  filters: TaskFilters
  onFilterChange: (filters: TaskFilters) => void
  masjids: Masjid[]
}
```

**Controls**:
- Category dropdown
- Priority dropdown
- Status radio buttons
- Masjid dropdown
- Search input
- Sort controls

### 2. Masjids Feature (Frontend)

#### **app/masjids/page.tsx** (REQUIRED - Main Masjids List)

**Purpose**: Display all masjids with area filtering

**Required Functionality**:
1. Fetch masjids from `/api/v1/masjids` on page load
2. Display masjids in responsive grid
3. Area filter dropdown (extract unique areas from masjid list)
4. City filter
5. Search box for masjid name
6. Each masjid card shows:
   - Masjid name
   - Area and city
   - Address
   - Imam name
   - Phone number
   - "View Details" button → `/masjids/{id}`
7. Loading state
8. Error state
9. Empty state

**Data Flow**:
```typescript
const masjids = await api.getMasjids({
  area: selectedArea,
  city: selectedCity,
  search: searchText,
})
```

**UI Requirements**:
- Responsive grid (1 col mobile, 2 col tablet, 3 col desktop)
- Area/city badges
- Phone click-to-call
- Location icon
- Hover effects

#### **app/masjids/[id]/page.tsx** (REQUIRED - Masjid Detail)

**Purpose**: View detailed information about a masjid

**Display**:
1. Masjid name (large heading)
2. Area and city
3. Full address
4. Imam name
5. Phone number (click-to-call)
6. Facilities (if available, parsed from JSON)
7. **Tasks associated with this masjid**:
   - Fetch tasks using `api.getMasjidTasks(masjidId)`
   - Display in compact list
   - Link to each task detail

**Actions**:
- "Back to Masjids" link
- "View All Tasks for this Masjid" link

**Data Flow**:
```typescript
const masjid = await api.getMasjid(masjidId)
const tasks = await api.getMasjidTasks(masjidId)
```

#### **app/masjids/components/MasjidList.tsx** (REQUIRED)

**Purpose**: Reusable component to display list of masjids

**Props**:
```typescript
interface MasjidListProps {
  masjids: Masjid[]
  onSelectMasjid: (masjid: Masjid) => void
}
```

#### **app/masjids/components/MasjidCard.tsx** (REQUIRED)

**Purpose**: Display individual masjid in card format

**Props**:
```typescript
interface MasjidCardProps {
  masjid: Masjid
  onClick?: (masjid: Masjid) => void
}
```

**Display**:
- Name, area, city
- Address, imam, phone
- View details button

#### **app/masjids/components/AreaFilter.tsx** (REQUIRED)

**Purpose**: Filter masjids by area

**Props**:
```typescript
interface AreaFilterProps {
  areas: string[]
  selectedArea: string | null
  onAreaChange: (area: string | null) => void
}
```

### 3. Hadith Feature (Frontend)

#### **app/hadith/page.tsx** (REQUIRED - Daily Hadith)

**Purpose**: Display today's hadith

**Display**:
1. Fetch today's hadith using `api.getTodaysHadith()`
2. Display:
   - Arabic text (right-to-left, larger font)
   - English translation
   - Narrator
   - Source (e.g., "Sahih Bukhari 1234")
   - Theme (if available)
3. Beautiful card design
4. Option to navigate to previous hadith entries

**Data Flow**:
```typescript
const hadith = await api.getTodaysHadith()
```

---

## Integration Requirements

### API Client (`lib/api.ts`)

**Status**: ✅ Already implemented and complete

The API client provides all necessary methods for:
- Tasks CRUD operations
- Masjids CRUD operations
- Hadith operations
- Bulk operations
- Filtering and pagination

**Base URL Configuration**:
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
```

### Environment Variables

**Backend** (`.env`):
```env
DATABASE_URL=postgresql://user:password@host:port/database
ENVIRONMENT=development
DEBUG=true
```

**Frontend** (`.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Error Handling

All frontend components must handle:
1. **Loading States**: Show spinner or skeleton
2. **Error States**: Display user-friendly error messages
3. **Network Errors**: Handle offline/timeout scenarios
4. **404 Not Found**: Redirect or show "Not Found" message
5. **Validation Errors**: Display field-level errors

Example:
```typescript
try {
  setLoading(true)
  const tasks = await api.getTasks(filters)
  setTasks(tasks)
  setError(null)
} catch (err) {
  setError('Failed to load tasks. Please try again.')
  console.error(err)
} finally {
  setLoading(false)
}
```

---

## API Contract Specifications

### Sample API Request/Response Examples

#### 1. GET /api/v1/tasks (List Tasks)

**Request**:
```http
GET /api/v1/tasks?category=Farz&priority=High&completed=false&sort_by=due_datetime&sort_order=asc
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Fajr Prayer at Masjid",
    "description": "Attend congregation prayer",
    "category": "Farz",
    "priority": "High",
    "tags": "prayer,congregation",
    "masjid_id": 5,
    "masjid": {
      "id": 5,
      "name": "Masjid Al-Noor",
      "area": "Downtown",
      "city": "Springfield"
    },
    "due_datetime": "2025-12-28T05:30:00Z",
    "recurrence": "Daily",
    "completed": false,
    "completed_at": null,
    "created_at": "2025-12-27T10:00:00Z",
    "updated_at": "2025-12-27T10:00:00Z"
  }
]
```

#### 2. POST /api/v1/tasks (Create Task)

**Request**:
```http
POST /api/v1/tasks
Content-Type: application/json

{
  "title": "Read Quran 1 page",
  "description": "Daily Quran reading routine",
  "category": "Sunnah",
  "priority": "Medium",
  "tags": "quran,daily",
  "masjid_id": null,
  "due_datetime": "2025-12-28T20:00:00Z",
  "recurrence": "Daily"
}
```

**Response** (201 Created):
```json
{
  "id": 42,
  "title": "Read Quran 1 page",
  "description": "Daily Quran reading routine",
  "category": "Sunnah",
  "priority": "Medium",
  "tags": "quran,daily",
  "masjid_id": null,
  "masjid": null,
  "due_datetime": "2025-12-28T20:00:00Z",
  "recurrence": "Daily",
  "completed": false,
  "completed_at": null,
  "created_at": "2025-12-27T18:30:00Z",
  "updated_at": "2025-12-27T18:30:00Z"
}
```

#### 3. GET /api/v1/masjids (List Masjids)

**Request**:
```http
GET /api/v1/masjids?area=Downtown
```

**Response** (200 OK):
```json
[
  {
    "id": 5,
    "name": "Masjid Al-Noor",
    "area": "Downtown",
    "city": "Springfield",
    "address": "123 Main Street",
    "imam_name": "Imam Abdullah",
    "phone": "+1-555-0100",
    "facilities": "{\"parking\": true, \"wudu\": true, \"library\": false}",
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:00:00Z"
  }
]
```

#### 4. GET /api/v1/masjids/{id}/tasks (Masjid Tasks)

**Request**:
```http
GET /api/v1/masjids/5/tasks?completed=false
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Fajr Prayer at Masjid",
    "category": "Farz",
    "priority": "High",
    "due_datetime": "2025-12-28T05:30:00Z",
    "completed": false
  }
]
```

#### 5. GET /api/v1/hadith/today (Today's Hadith)

**Request**:
```http
GET /api/v1/hadith/today
```

**Response** (200 OK):
```json
{
  "id": 123,
  "hadith_date": "2025-12-27",
  "arabic_text": "إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ",
  "english_translation": "Actions are judged by intentions",
  "narrator": "Umar ibn Al-Khattab",
  "source": "Sahih Bukhari 1",
  "theme": "Intention",
  "created_at": "2025-12-27T00:00:00Z"
}
```

---

## Acceptance Criteria

### Backend Acceptance Criteria

✅ **Tasks Module**:
- [ ] All 11 endpoints respond successfully
- [ ] Filtering works for category, priority, completed, masjid_id, search
- [ ] Sorting works for due_datetime, priority, title, created_at
- [ ] Bulk operations (complete, delete) work correctly
- [ ] Statistics endpoint returns accurate counts
- [ ] Database relationships (task → masjid) work correctly

✅ **Masjids Module**:
- [ ] All 6 endpoints respond successfully
- [ ] Filtering by city, area, search works
- [ ] GET /masjids/{id}/tasks returns tasks for specific masjid
- [ ] Masjid CRUD operations work correctly

✅ **Hadith Module**:
- [ ] All 7 endpoints respond successfully
- [ ] GET /hadith/today returns today's hadith
- [ ] Date-based retrieval works
- [ ] Unique constraint on hadith_date enforced

### Frontend Acceptance Criteria

✅ **Tasks Feature - NOT EMPTY**:
- [ ] `/tasks` page exists and displays list of tasks
- [ ] `/tasks/new` page exists with working create form
- [ ] `/tasks/{id}` page exists and shows task details
- [ ] `/tasks/{id}/edit` page exists with working edit form
- [ ] `app/tasks/components/` folder contains at least 4 working components:
  - [ ] TaskList.tsx
  - [ ] TaskForm.tsx
  - [ ] TaskCard.tsx
  - [ ] TaskFilters.tsx
- [ ] All components compile without errors
- [ ] Filtering, sorting, search work correctly
- [ ] Create, edit, delete operations work
- [ ] Mark complete/incomplete works
- [ ] Loading states display correctly
- [ ] Error states display user-friendly messages

✅ **Masjids Feature - NOT EMPTY**:
- [ ] `/masjids` page exists and displays list of masjids
- [ ] `/masjids/{id}` page exists and shows masjid details with associated tasks
- [ ] `app/masjids/components/` folder contains at least 3 working components:
  - [ ] MasjidList.tsx
  - [ ] MasjidCard.tsx
  - [ ] AreaFilter.tsx
- [ ] All components compile without errors
- [ ] Area filtering works
- [ ] Masjid detail page shows tasks for that masjid
- [ ] Loading and error states work

✅ **Hadith Feature**:
- [ ] `/hadith` page exists and displays today's hadith
- [ ] Arabic text displays right-to-left
- [ ] Translation, narrator, source display correctly

### Integration Acceptance Criteria

✅ **API Integration**:
- [ ] Frontend successfully calls backend endpoints
- [ ] Data fetched from backend displays correctly in UI
- [ ] Create/update operations persist to database
- [ ] Delete operations remove data from database
- [ ] Error responses from backend handled gracefully in frontend

### Manual Testing Scenarios

**Scenario 1: Create a Spiritual Task**
1. Navigate to `/tasks/new`
2. Fill in task details (title, category, priority, masjid, due date)
3. Click "Create Task"
4. Verify task appears in `/tasks` list
5. Verify task appears in database
6. Verify task appears under masjid detail page (if masjid selected)

**Scenario 2: Filter Tasks by Masjid**
1. Navigate to `/tasks`
2. Select a masjid from filter dropdown
3. Verify only tasks for that masjid display
4. Clear filter
5. Verify all tasks display again

**Scenario 3: View Masjid Details with Tasks**
1. Navigate to `/masjids`
2. Click on a masjid card
3. Navigate to `/masjids/{id}`
4. Verify masjid details display
5. Verify associated tasks display in list
6. Click on a task link
7. Verify navigation to `/tasks/{id}` works

**Scenario 4: Complete a Task**
1. Navigate to `/tasks`
2. Click "Mark Complete" on a task
3. Verify task status changes to completed
4. Verify completed_at timestamp set in database
5. Filter by "Completed" status
6. Verify task appears in completed list

**Scenario 5: View Daily Hadith**
1. Navigate to `/hadith`
2. Verify today's hadith displays
3. Verify Arabic text and English translation visible
4. Verify narrator and source displayed

---

## Implementation Checklist

### Phase 1: Backend Verification ✅
- [x] Verify all models in `models.py` are correct
- [x] Verify `routers/tasks.py` has all 11 endpoints
- [x] Verify `routers/masjids.py` has all 6 endpoints
- [x] Verify `routers/hadith.py` has all 7 endpoints
- [x] Test all endpoints with sample requests
- [x] Verify database migrations are up to date

### Phase 2: Frontend Core Structure 🔨
- [x] Create `app/layout.tsx` and `app/page.tsx` ✅
- [x] Create `lib/api.ts` and `lib/types.ts` ✅
- [ ] Create `lib/utils.ts` for helper functions
- [ ] Move shared components to appropriate locations

### Phase 3: Tasks Feature Implementation 🔨
- [ ] Create `app/tasks/page.tsx` (list)
- [ ] Create `app/tasks/new/page.tsx` (create)
- [ ] Create `app/tasks/[id]/page.tsx` (detail)
- [ ] Create `app/tasks/[id]/edit/page.tsx` (edit)
- [ ] Create `app/tasks/components/TaskList.tsx`
- [ ] Create `app/tasks/components/TaskForm.tsx`
- [ ] Create `app/tasks/components/TaskCard.tsx`
- [ ] Create `app/tasks/components/TaskFilters.tsx`
- [ ] Test all task pages and components
- [ ] Verify no TypeScript errors
- [ ] Verify folder is NOT empty

### Phase 4: Masjids Feature Implementation 🔨
- [ ] Create `app/masjids/page.tsx` (list)
- [ ] Create `app/masjids/[id]/page.tsx` (detail)
- [ ] Create `app/masjids/components/MasjidList.tsx`
- [ ] Create `app/masjids/components/MasjidCard.tsx`
- [ ] Create `app/masjids/components/AreaFilter.tsx`
- [ ] Test all masjid pages and components
- [ ] Verify no TypeScript errors
- [ ] Verify folder is NOT empty

### Phase 5: Hadith Feature Implementation 🔨
- [ ] Create `app/hadith/page.tsx`
- [ ] Style Arabic text properly (RTL, larger font)
- [ ] Test hadith display

### Phase 6: Integration Testing 🔨
- [ ] Test create task flow end-to-end
- [ ] Test edit task flow end-to-end
- [ ] Test delete task flow
- [ ] Test task filtering and sorting
- [ ] Test masjid listing with area filter
- [ ] Test masjid detail with associated tasks
- [ ] Test hadith display
- [ ] Verify loading states
- [ ] Verify error handling
- [ ] Test on mobile, tablet, desktop

### Phase 7: Final Verification ✅
- [ ] Run `npm run build` successfully
- [ ] Run `npm run lint` with no errors
- [ ] Verify all acceptance criteria met
- [ ] Verify no empty folders
- [ ] Verify all components compile
- [ ] Manual testing of all user flows

---

## Success Metrics

The implementation is considered **COMPLETE** when:

1. ✅ Backend has 24 working endpoints (11 tasks + 6 masjids + 7 hadith)
2. ✅ Frontend `tasks` folder contains **at least 8 files** with working code:
   - 4 page files (list, new, detail, edit)
   - 4 component files (TaskList, TaskForm, TaskCard, TaskFilters)
3. ✅ Frontend `masjids` folder contains **at least 5 files** with working code:
   - 2 page files (list, detail)
   - 3 component files (MasjidList, MasjidCard, AreaFilter)
4. ✅ Frontend `hadith` folder contains **at least 1 page file** with working code
5. ✅ All pages compile without TypeScript errors
6. ✅ All acceptance criteria tests pass
7. ✅ All manual testing scenarios complete successfully
8. ✅ `npm run build` completes without errors

---

## Non-Negotiable Requirements

1. **NO EMPTY FOLDERS**: The `tasks` and `masjids` folders in the frontend **must contain working code**, not empty stubs.
2. **NO PLACEHOLDERS**: All components must have real implementation, not just "TODO" comments.
3. **NO BROKEN BUILDS**: All code must compile and run without errors.
4. **WORKING API INTEGRATION**: Frontend must successfully fetch and display data from backend.
5. **COMPLETE CRUD**: All create, read, update, delete operations must work for both tasks and masjids.

---

## Document Control

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-12-27 | Initial specification | AI Assistant |
| 2.0 | 2025-12-27 | Refined with explicit folder structure and acceptance criteria | AI Assistant |

---

**END OF SPECIFICATION**
