# SalaatFlow Phase II - Quick Implementation Guide

**For**: Human Developer & Claude Code Assistant
**Goal**: Ensure Tasks and Masjids features are fully implemented, not empty stubs

---

## Current Status

### ✅ Already Implemented (Working)

**Backend**:
- `models.py` - All database models (SpiritualTask, Masjid, DailyHadith)
- `routers/tasks.py` - 11 complete endpoints
- `routers/masjids.py` - 6 complete endpoints
- `routers/hadith.py` - 7 complete endpoints
- Database migrations via Alembic
- PostgreSQL on Neon

**Frontend Foundation**:
- `app/layout.tsx` - Root layout
- `app/page.tsx` - Home page
- `lib/api.ts` - Complete API client
- `lib/types.ts` - TypeScript interfaces
- `components/Navbar.tsx` - Navigation
- `components/TaskCard.tsx` - Task card component

### ❌ Missing (Must Be Implemented)

**Frontend - Tasks Feature** (`app/tasks/`):
- [ ] `app/tasks/page.tsx` - List all tasks with filters
- [ ] `app/tasks/new/page.tsx` - Create task form
- [ ] `app/tasks/[id]/page.tsx` - Task detail view
- [ ] `app/tasks/[id]/edit/page.tsx` - Edit task form
- [ ] `app/tasks/components/TaskList.tsx`
- [ ] `app/tasks/components/TaskForm.tsx`
- [ ] `app/tasks/components/TaskCard.tsx`
- [ ] `app/tasks/components/TaskFilters.tsx`

**Frontend - Masjids Feature** (`app/masjids/`):
- [ ] `app/masjids/page.tsx` - List all masjids
- [ ] `app/masjids/[id]/page.tsx` - Masjid detail + tasks
- [ ] `app/masjids/components/MasjidList.tsx`
- [ ] `app/masjids/components/MasjidCard.tsx`
- [ ] `app/masjids/components/AreaFilter.tsx`

**Frontend - Hadith Feature** (`app/hadith/`):
- [ ] `app/hadith/page.tsx` - Today's hadith display

---

## Implementation Order

### Step 1: Create Utils (5 minutes)

Create `lib/utils.ts`:
```typescript
// Date formatting
export function formatDate(dateString: string): string
export function formatDateTime(dateString: string): string
export function isOverdue(dueDate: string): boolean

// Priority colors
export function getPriorityColor(priority: Priority): string

// Category badges
export function getCategoryBadgeColor(category: TaskCategory): string
```

### Step 2: Tasks Feature (60 minutes)

1. **List Page** (`app/tasks/page.tsx`):
   - Client component ('use client')
   - Fetch tasks with `api.getTasks()`
   - Render TaskList component
   - Add filters with TaskFilters component
   - Loading spinner, error message, empty state

2. **Create Page** (`app/tasks/new/page.tsx`):
   - Client component
   - Render TaskForm with no initial data
   - On submit: `api.createTask(data)`, then navigate to `/tasks`

3. **Detail Page** (`app/tasks/[id]/page.tsx`):
   - Fetch task with `api.getTask(id)`
   - Display all fields
   - "Edit", "Complete", "Delete" buttons

4. **Edit Page** (`app/tasks/[id]/edit/page.tsx`):
   - Fetch task, pass to TaskForm as initialData
   - On submit: `api.updateTask(id, data)`, then navigate back

5. **Components**:
   - **TaskList**: Map over tasks array, render TaskCard for each
   - **TaskForm**: All fields, validation, submit handler
   - **TaskCard**: Display task info, quick actions
   - **TaskFilters**: Dropdowns for category, priority, status, search input

### Step 3: Masjids Feature (45 minutes)

1. **List Page** (`app/masjids/page.tsx`):
   - Client component
   - Fetch masjids with `api.getMasjids()`
   - Area filter dropdown
   - Render MasjidList component

2. **Detail Page** (`app/masjids/[id]/page.tsx`):
   - Fetch masjid with `api.getMasjid(id)`
   - Fetch tasks with `api.getMasjidTasks(id)`
   - Display masjid info
   - Display associated tasks in list

3. **Components**:
   - **MasjidList**: Map over masjids, render MasjidCard
   - **MasjidCard**: Display masjid info, click to view details
   - **AreaFilter**: Extract unique areas, dropdown select

### Step 4: Hadith Feature (15 minutes)

1. **Hadith Page** (`app/hadith/page.tsx`):
   - Fetch today's hadith with `api.getTodaysHadith()`
   - Display in beautiful card
   - Arabic text: larger font, RTL
   - English translation below
   - Narrator, source, theme

### Step 5: Testing (30 minutes)

1. Run `npm run dev` and visit each page
2. Test create task flow
3. Test edit task flow
4. Test delete task
5. Test filters on tasks page
6. Test masjid detail shows tasks
7. Test hadith display
8. Verify no console errors
9. Run `npm run build` - must succeed

---

## File Structure to Create

```
frontend/app/
├── tasks/
│   ├── page.tsx                 # List (main)
│   ├── new/
│   │   └── page.tsx             # Create
│   ├── [id]/
│   │   ├── page.tsx             # Detail
│   │   └── edit/
│   │       └── page.tsx         # Edit
│   └── components/
│       ├── TaskList.tsx         # List component
│       ├── TaskForm.tsx         # Form component
│       ├── TaskCard.tsx         # Card component
│       └── TaskFilters.tsx      # Filters component
│
├── masjids/
│   ├── page.tsx                 # List (main)
│   ├── [id]/
│   │   └── page.tsx             # Detail
│   └── components/
│       ├── MasjidList.tsx       # List component
│       ├── MasjidCard.tsx       # Card component
│       └── AreaFilter.tsx       # Filter component
│
└── hadith/
    └── page.tsx                 # Today's hadith
```

---

## API Usage Examples

### Tasks

```typescript
// List tasks with filters
const tasks = await api.getTasks({
  category: TaskCategory.FARZ,
  priority: Priority.HIGH,
  completed: false,
  search: "prayer",
  sort_by: "due_datetime",
  sort_order: "asc"
})

// Get single task
const task = await api.getTask(1)

// Create task
const newTask = await api.createTask({
  title: "Fajr Prayer",
  category: TaskCategory.FARZ,
  priority: Priority.HIGH,
  recurrence: Recurrence.DAILY,
  due_datetime: "2025-12-28T05:30:00Z"
})

// Update task
const updated = await api.updateTask(1, { completed: true })

// Delete task
await api.deleteTask(1)
```

### Masjids

```typescript
// List masjids
const masjids = await api.getMasjids({
  area: "Downtown",
  search: "Al-Noor"
})

// Get single masjid
const masjid = await api.getMasjid(5)

// Get tasks for masjid
const tasks = await api.getMasjidTasks(5, false) // false = pending only
```

### Hadith

```typescript
// Get today's hadith
const hadith = await api.getTodaysHadith()
```

---

## Component Templates

### Client Component Template

```typescript
'use client'

import { useState, useEffect } from 'react'
import api from '@/lib/api'
import { SpiritualTask } from '@/lib/types'

export default function TasksPage() {
  const [tasks, setTasks] = useState<SpiritualTask[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchTasks()
  }, [])

  const fetchTasks = async () => {
    try {
      setLoading(true)
      const data = await api.getTasks()
      setTasks(data)
      setError(null)
    } catch (err) {
      setError('Failed to load tasks')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div>
      <h1>Tasks</h1>
      {/* Render tasks */}
    </div>
  )
}
```

### Form Component Template

```typescript
'use client'

import { useState } from 'react'
import { TaskFormData, TaskCategory, Priority, Recurrence } from '@/lib/types'

interface TaskFormProps {
  initialData?: TaskFormData
  onSubmit: (data: TaskFormData) => Promise<void>
  onCancel: () => void
}

export default function TaskForm({ initialData, onSubmit, onCancel }: TaskFormProps) {
  const [formData, setFormData] = useState<TaskFormData>(
    initialData || {
      title: '',
      category: TaskCategory.OTHER,
      priority: Priority.MEDIUM,
      recurrence: Recurrence.NONE,
    }
  )

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={formData.title}
        onChange={(e) => setFormData({ ...formData, title: e.target.value })}
        required
      />
      {/* More form fields */}
      <button type="submit">Submit</button>
      <button type="button" onClick={onCancel}>Cancel</button>
    </form>
  )
}
```

---

## Styling Guidelines

Use Tailwind CSS classes:

- **Cards**: `bg-white rounded-lg shadow-md p-6`
- **Buttons**: `bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700`
- **Badges**: `inline-block px-3 py-1 text-sm rounded-full`
- **Priority Colors**:
  - Urgent: `bg-red-100 text-red-800`
  - High: `bg-orange-100 text-orange-800`
  - Medium: `bg-yellow-100 text-yellow-800`
  - Low: `bg-green-100 text-green-800`

---

## Verification Commands

```bash
# Backend - verify running
curl http://localhost:8000/api/v1/tasks

# Frontend - build test
cd frontend
npm run build

# Frontend - lint test
npm run lint

# Frontend - dev server
npm run dev
```

---

## Success Criteria

✅ **DONE when**:

1. All 8 task pages/components created
2. All 5 masjid pages/components created
3. Hadith page created
4. All pages compile without TypeScript errors
5. `npm run build` succeeds
6. Manual testing: can create, view, edit, delete tasks
7. Manual testing: can view masjids and their associated tasks
8. Manual testing: can view daily hadith
9. **NO EMPTY FOLDERS** - all contain working code

---

## Common Issues & Solutions

**Issue**: "Module not found: Can't resolve '@/lib/api'"
**Solution**: Verify `tsconfig.json` has path mapping:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

**Issue**: API calls fail with CORS error
**Solution**: Ensure backend has CORS middleware configured in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Issue**: "Hydration failed" error
**Solution**: Ensure client components use 'use client' directive at top of file

**Issue**: TypeScript errors on api calls
**Solution**: Import types from `@/lib/types`

---

**REMEMBER**: The goal is to have **working, functional code** in every folder, not empty stubs or placeholders. Every component must compile and render without errors.
