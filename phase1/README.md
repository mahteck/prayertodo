# SalaatFlow - Phase I: Console Edition

**Prayer & Spiritual Task Manager**

An Islamic prayer and spiritual task management system designed to help Muslims organize their religious obligations, good deeds, and masjid-related activities.

---

## Project Description

SalaatFlow is a Todo system specialized for Islamic spiritual practices. Phase I provides an in-memory Python console application for managing spiritual tasks including:

- **Prayer obligations** (Farz, Sunnah, Nafl)
- **Good deeds and charity** (Sadqah, helping others)
- **Masjid-specific tasks** with area/location tracking
- **Quranic recitation reminders**
- **General spiritual to-dos**

This is Phase I of a 5-phase evolution from console app → web app → AI chatbot → Kubernetes → cloud deployment.

---

## Installation

### Requirements
- **Python 3.11 or higher**
- **No external dependencies** - uses Python standard library only

### Setup
1. Clone or download the project
2. Navigate to the phase1 directory:
   ```bash
   cd phase1
   ```
3. Run the application:
   ```bash
   python3 main.py
   ```

---

## Usage

### Starting the Application

```bash
python3 phase1/main.py
```

You'll see the welcome banner and help text:

```
========================================
  SalaatFlow - Prayer & Spiritual Tasks
  Phase I: Console Edition
========================================

SalaatFlow - Prayer & Spiritual Task Manager
Available Commands:
  add              - Add a new spiritual task
  list [filter]    - List all tasks (filter: all|pending|completed)
  view <id>        - View detailed information for a task
  update <id>      - Update an existing task
  delete <id>      - Delete a task by ID
  complete <id>    - Mark a task as completed
  uncomplete <id>  - Mark a task as incomplete
  help             - Show this help message
  exit             - Exit the application

salaatflow>
```

---

## Command Reference

### `help`
Display list of available commands.

**Usage**: `help`

---

### `add`
Add a new spiritual task with interactive prompts.

**Usage**: `add`

**Prompts**:
- **Title** (required): Task name (max 200 chars)
- **Description** (optional): Additional details
- **Category** (required): Select from:
  1. **Farz** (فرض): Obligatory acts (e.g., five daily prayers)
  2. **Sunnah** (سنّة): Practices of Prophet Muhammad (ﷺ)
  3. **Nafl** (نفل): Voluntary worship acts
  4. **Deed**: General good deeds (charity, helping others)
- **Masjid** (optional): Associated masjid name
- **Area** (optional): Location/neighborhood
- **Due Date/Time** (optional): Format YYYY-MM-DD HH:MM (e.g., 2025-12-28 05:30)

**Example**:
```
salaatflow> add
Enter task title (required): Attend Fajr at Masjid Al-Noor
Enter description (optional, press Enter to skip): Wake up 30 minutes early
Select category:
  1. Farz
  2. Sunnah
  3. Nafl
  4. Deed
Enter choice (1-4): 1
Enter masjid name (optional): Masjid Al-Noor
Enter area name (optional): DHA Phase 5
Enter due date/time (optional, format: YYYY-MM-DD HH:MM or press Enter to skip): 2025-12-28 05:30

Task added successfully! (ID: 1)
```

---

### `list [filter]`
List tasks with optional filtering.

**Usage**:
- `list` - Show all tasks (default)
- `list all` - Show all tasks
- `list pending` - Show only incomplete tasks
- `list completed` - Show only completed tasks

**Example**:
```
salaatflow> list pending

ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
1  | [ ]    | Farz     | Attend Fajr at Masjid Al-Noor | Masjid Al-Noor   | DHA Phase 5  | 2025-12-28 05:30
2  | [ ]    | Deed     | Give charity today             | -                | -            | -

Total: 2 tasks (0 completed, 2 pending)
```

---

### `view <id>`
View detailed information for a specific task.

**Usage**: `view <id>`

**Example**:
```
salaatflow> view 1

Task ID: 1
Title: Attend Fajr at Masjid Al-Noor
Description: Wake up 30 minutes early
Category: Farz
Masjid: Masjid Al-Noor
Area: DHA Phase 5
Due Date/Time: 2025-12-28 05:30
Status: Pending
Created: 2025-12-27 10:00:00
Last Updated: 2025-12-27 10:00:00
```

---

### `update <id>`
Update an existing task with interactive prompts.

**Usage**: `update <id>`

Shows current values and allows you to press Enter to keep them or enter new values.

**Example**:
```
salaatflow> update 1

Updating Task ID: 1

Current title: Attend Fajr at Masjid Al-Noor
New title (press Enter to keep current):

Current description: Wake up 30 minutes early
New description (press Enter to keep current): Prepare wudu before leaving

...

Task updated successfully!
```

---

### `delete <id>`
Delete a task after confirmation.

**Usage**: `delete <id>`

**Example**:
```
salaatflow> delete 2

Are you sure you want to delete this task?
  ID: 2
  Title: Give charity today
Confirm deletion? (y/n): y

Task deleted successfully!
```

---

### `complete <id>`
Mark a task as completed.

**Usage**: `complete <id>`

**Example**:
```
salaatflow> complete 1
Task ID 1 marked as completed!
```

---

### `uncomplete <id>`
Mark a task as incomplete (undo completion).

**Usage**: `uncomplete <id>`

**Example**:
```
salaatflow> uncomplete 1
Task ID 1 marked as incomplete!
```

---

### `exit`
Exit the application.

**Usage**: `exit`

Displays farewell message: "JazakAllah Khair for using SalaatFlow! May your deeds be accepted."

---

## Example Usage Session

Here's a typical workflow:

```bash
$ python3 phase1/main.py

========================================
  SalaatFlow - Prayer & Spiritual Tasks
  Phase I: Console Edition
========================================

SalaatFlow - Prayer & Spiritual Task Manager
Available Commands:
  ...

salaatflow> add
Enter task title (required): Attend Fajr at Masjid Al-Huda
...
Task added successfully! (ID: 1)

salaatflow> add
Enter task title (required): Read Surah Yaseen
...
Task added successfully! (ID: 2)

salaatflow> list

ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
1  | [ ]    | Farz     | Attend Fajr at Masjid Al-Huda | Masjid Al-Huda   | DHA Phase 5  | 2025-12-28 05:30
2  | [ ]    | Sunnah   | Read Surah Yaseen              | -                | -            | -

Total: 2 tasks (0 completed, 2 pending)

salaatflow> complete 1
Task ID 1 marked as completed!

salaatflow> list completed

ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
1  | [✓]    | Farz     | Attend Fajr at Masjid Al-Huda | Masjid Al-Huda   | DHA Phase 5  | 2025-12-28 05:30

Total: 1 task (1 completed, 0 pending)

salaatflow> exit
JazakAllah Khair for using SalaatFlow! May your deeds be accepted.
```

---

## Domain Explanation

### Spiritual Tasks
A "task" in SalaatFlow represents any Islamic spiritual practice or religious obligation, such as:
- Attending prayers at the masjid
- Quranic recitation
- Giving charity (Sadqah)
- Acts of kindness and good deeds
- Dhikr (remembrance of Allah)
- Islamic study sessions

### Category Meanings

| Category | Arabic | Meaning | Examples |
|----------|--------|---------|----------|
| **Farz** | فرض | Obligatory acts | Five daily prayers, Jummah prayer |
| **Sunnah** | سنّة | Practices of Prophet Muhammad (ﷺ) | Sunnah prayers, reading Ayat-ul-Kursi before sleep |
| **Nafl** | نفل | Voluntary worship acts | Extra prayers, voluntary fasting, Tahajjud |
| **Deed** | - | General good deeds | Charity, helping neighbors, visiting sick |

### Masjid & Area Fields
- **Masjid**: Name of the mosque (e.g., "Masjid Al-Noor", "Central Jamia Masjid")
- **Area**: Locality or neighborhood (e.g., "DHA Phase 5", "Gulshan-e-Iqbal", "Clifton")

These fields help organize tasks by location, especially useful for prayer timings at different masjids.

---

## Phase I Scope and Limitations

### What's Included ✅
- In-memory task storage (not persisted to disk)
- Full CRUD operations (Create, Read, Update, Delete)
- Task completion tracking
- Filtering by completion status
- Input validation
- Error handling
- Islamic terminology and categories

### What's NOT Included ❌
- **No persistent storage** - tasks lost when app closes
- **No masjid database** - masjid/area are free text fields
- **No prayer time lookup** - due times entered manually
- **No recurring tasks** - each task created individually
- **No reminders or notifications**
- **No web UI** - console only
- **No multi-user support**
- **No authentication**

These features will be added in later phases (II-V).

---

## What's Next - Phase II Preview

Phase II will introduce:
- **Persistent storage** with Neon PostgreSQL database
- **Full-stack web app** with Next.js frontend and FastAPI backend
- **REST API** for task management
- **Web UI** with modern React components
- **Advanced filtering** by date ranges, categories, masjids

---

## Technical Details

### File Structure
```
phase1/
├── main.py              # Entry point, REPL loop
├── models.py            # Task data model and constants
├── storage.py           # In-memory storage manager
├── commands.py          # Command handlers
├── validators.py        # Input validation functions
├── display.py           # Output formatting
├── README.md            # This file
└── TESTING.md           # Test documentation
```

### Data Model
Each task stores:
- `id` (int): Auto-incremented unique identifier
- `title` (str): Task name (required, max 200 chars)
- `description` (str): Optional details
- `category` (str): Farz/Sunnah/Nafl/Deed
- `masjid_name` (str): Optional masjid name
- `area_name` (str): Optional area/location
- `due_datetime` (datetime): Optional deadline
- `completed` (bool): Completion status
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last modification timestamp

### Python Version
- **Required**: Python 3.11+
- **Dependencies**: Standard library only (datetime, typing)

---

## Testing

See [`TESTING.md`](./TESTING.md) for comprehensive test scenarios and manual testing instructions.

---

## Links

- **Full Specification**: `/specs/phase1-cli.md`
- **Implementation Plan**: `/plans/phase1-plan.md`
- **Task List**: `/tasks/phase1-tasks.md`
- **Project Constitution**: `/specs/constitution.md`

---

## License & Attribution

Part of the **SalaatFlow** project - A 5-phase hackathon evolution of Islamic task management.

**May Allah accept our efforts and make this tool beneficial for the Muslim Ummah.**

---

**Last Updated**: 2025-12-27
**Phase**: I - Console Edition
**Status**: ✅ Complete and Ready for Demo
