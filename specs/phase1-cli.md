# Phase I Specification – SalaatFlow In-Memory Python Console App

**Project**: SalaatFlow – Intelligent Prayer & Masjid Todo Assistant
**Phase**: I – In-Memory Python Console Application
**Version**: 1.0
**Date**: 2025-12-27
**Status**: Approved for Implementation

---

## 1. Phase I Constitution – Prayer & Spiritual Tasks

### 1.1 Purpose
Phase I establishes the **core domain model** for spiritual task management using a pure Python console application. This phase validates the domain logic and user workflows before adding persistence, web interfaces, or AI capabilities.

### 1.2 Scope
**In Scope:**
- In-memory CRUD operations for spiritual tasks
- Interactive CLI with menu-driven and command-based interfaces
- Task categorization by Islamic practice types (Farz, Sunnah, Nafl, Deed)
- Optional masjid and area associations (free text)
- Task completion status tracking
- Basic filtering (completed vs. pending)
- Input validation and error handling

**Out of Scope:**
- Persistent storage (database or file system)
- Masjid database or timetable lookup
- Web UI or API
- AI chatbot or natural language processing
- Recurring tasks (deferred to Phase III)
- Reminders or notifications
- User authentication
- Multi-user support

### 1.3 Domain Alignment
This application satisfies the "Evolution of Todo" basic requirements through the Islamic spiritual task domain:
- **Add Task** → Add spiritual obligation or good deed
- **Delete Task** → Remove task by ID
- **Update Task** → Modify task properties
- **View Tasks** → List all or filtered tasks
- **Complete Task** → Mark task as done

### 1.4 Design Principles
- **Simplicity First**: Console-only, no external dependencies beyond Python standard library
- **Domain-Driven**: Use Islamic terminology naturally (Farz, Masjid, etc.)
- **Extensibility**: Data model designed to evolve into Phase II database schema
- **User-Friendly**: Clear prompts, helpful error messages, input validation

---

## 2. Data Model

### 2.1 Task Entity

The core entity is a **Spiritual Task** represented as a Python dictionary or dataclass with the following fields:

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `id` | `int` | Yes | Auto-incremented unique identifier | `1`, `2`, `3` |
| `title` | `str` | Yes | Task name (max 200 chars) | `"Attend Fajr at Masjid Al-Huda"` |
| `description` | `str` | No | Additional details (max 1000 chars) | `"Wake up 30 min early"` |
| `category` | `str` | Yes | Islamic practice type | `"Farz"`, `"Sunnah"`, `"Nafl"`, `"Deed"` |
| `masjid_name` | `str` | No | Associated masjid (free text, max 100 chars) | `"Masjid Al-Noor"` |
| `area_name` | `str` | No | Location/area (free text, max 100 chars) | `"DHA Phase 5"` |
| `due_datetime` | `datetime` | No | Optional deadline or prayer time | `datetime(2025, 12, 28, 5, 30)` |
| `completed` | `bool` | Yes | Completion status (default `False`) | `True`, `False` |
| `created_at` | `datetime` | Yes | Creation timestamp (auto-generated) | `datetime.now()` |
| `updated_at` | `datetime` | Yes | Last update timestamp (auto-updated) | `datetime.now()` |

### 2.2 Category Enumeration

Valid categories (case-insensitive input, stored in title case):
- **Farz** (فرض): Obligatory acts (e.g., five daily prayers)
- **Sunnah** (سنّة): Practices of Prophet Muhammad (ﷺ)
- **Nafl** (نفل): Voluntary worship acts
- **Deed**: General good deeds (charity, helping others, etc.)

### 2.3 In-Memory Storage

Tasks stored in a Python list: `tasks: List[dict]`

Auto-incrementing ID counter: `next_id: int`

Example:
```python
tasks = [
    {
        "id": 1,
        "title": "Attend Fajr at Masjid Al-Huda",
        "description": "Wake up 30 minutes early",
        "category": "Farz",
        "masjid_name": "Masjid Al-Huda",
        "area_name": "DHA Phase 5",
        "due_datetime": datetime(2025, 12, 28, 5, 30),
        "completed": False,
        "created_at": datetime(2025, 12, 27, 10, 0, 0),
        "updated_at": datetime(2025, 12, 27, 10, 0, 0)
    }
]
next_id = 2
```

---

## 3. CLI Commands & Behavior

### 3.1 Command Interface

The application runs in a **REPL (Read-Eval-Print Loop)** with two interaction modes:

1. **Command Mode**: User types commands like `list`, `add`, `delete 1`
2. **Interactive Mode**: Multi-step prompts for data entry (used by `add` and `update`)

### 3.2 Command Reference

#### 3.2.1 `help`
**Usage**: `help`

**Behavior**: Display list of available commands with brief descriptions.

**Output**:
```
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
```

---

#### 3.2.2 `add`
**Usage**: `add`

**Behavior**:
- Enter interactive mode with prompts for each field
- Required fields: title, category
- Optional fields: description, masjid_name, area_name, due_datetime
- Auto-generate `id`, `created_at`, `updated_at`
- Set `completed = False` by default

**Interactive Prompts**:
```
Enter task title (required): Attend Fajr at Masjid Al-Huda
Enter description (optional, press Enter to skip): Wake up 30 minutes early
Select category:
  1. Farz
  2. Sunnah
  3. Nafl
  4. Deed
Enter choice (1-4): 1
Enter masjid name (optional): Masjid Al-Huda
Enter area name (optional): DHA Phase 5
Enter due date/time (optional, format: YYYY-MM-DD HH:MM or press Enter to skip): 2025-12-28 05:30

Task added successfully! (ID: 1)
```

**Validation**:
- Title: 1-200 characters, non-empty
- Category: Must be one of the 4 valid options
- Due datetime: Must match format `YYYY-MM-DD HH:MM` or be empty

**Error Handling**:
- Invalid category choice → Re-prompt
- Invalid datetime format → Re-prompt or skip
- Empty title → Re-prompt

---

#### 3.2.3 `list [filter]`
**Usage**:
- `list` (default: show all)
- `list all`
- `list pending`
- `list completed`

**Behavior**: Display tasks in table format with filtering.

**Output Format**:
```
ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
1  | [ ]    | Farz     | Attend Fajr at Masjid Al-Huda | Masjid Al-Huda   | DHA Phase 5  | 2025-12-28 05:30
2  | [✓]    | Deed     | Give charity today             | -                | -            | -
3  | [ ]    | Sunnah   | Read Surah Yaseen after Fajr   | -                | -            | -

Total: 3 tasks (1 completed, 2 pending)
```

**Filtering**:
- `all`: Show all tasks
- `pending`: Show only tasks where `completed == False`
- `completed`: Show only tasks where `completed == True`

**Edge Cases**:
- No tasks → Display: `No tasks found.`
- No tasks match filter → Display: `No tasks found matching filter: {filter}`

---

#### 3.2.4 `view <id>`
**Usage**: `view 1`

**Behavior**: Display detailed information for a single task.

**Output**:
```
Task ID: 1
Title: Attend Fajr at Masjid Al-Huda
Description: Wake up 30 minutes early
Category: Farz
Masjid: Masjid Al-Huda
Area: DHA Phase 5
Due Date/Time: 2025-12-28 05:30
Status: Pending
Created: 2025-12-27 10:00:00
Last Updated: 2025-12-27 10:00:00
```

**Error Handling**:
- Task ID not found → Display: `Error: Task with ID {id} not found.`
- Invalid ID format → Display: `Error: Invalid task ID. Please enter a number.`

---

#### 3.2.5 `update <id>`
**Usage**: `update 1`

**Behavior**:
- Fetch task by ID
- Enter interactive mode showing current values
- Allow user to keep existing value (press Enter) or enter new value
- Update `updated_at` timestamp

**Interactive Prompts**:
```
Updating Task ID: 1

Current title: Attend Fajr at Masjid Al-Huda
New title (press Enter to keep current):

Current description: Wake up 30 minutes early
New description (press Enter to keep current): Prepare wudu before leaving

Current category: Farz
Select new category (press Enter to keep current):
  1. Farz
  2. Sunnah
  3. Nafl
  4. Deed
Enter choice (1-4) or press Enter:

Current masjid: Masjid Al-Huda
New masjid (press Enter to keep current):

Current area: DHA Phase 5
New area (press Enter to keep current):

Current due date/time: 2025-12-28 05:30
New due date/time (format: YYYY-MM-DD HH:MM, press Enter to keep current):

Task updated successfully!
```

**Validation**: Same as `add` command

**Error Handling**:
- Task ID not found → Display: `Error: Task with ID {id} not found.`

---

#### 3.2.6 `delete <id>`
**Usage**: `delete 1`

**Behavior**:
- Confirm deletion with user
- Remove task from list

**Confirmation Prompt**:
```
Are you sure you want to delete this task?
  ID: 1
  Title: Attend Fajr at Masjid Al-Huda
Confirm deletion? (y/n): y

Task deleted successfully!
```

**Error Handling**:
- Task ID not found → Display: `Error: Task with ID {id} not found.`
- User cancels (enters 'n') → Display: `Deletion cancelled.`

---

#### 3.2.7 `complete <id>`
**Usage**: `complete 1`

**Behavior**:
- Set `completed = True`
- Update `updated_at` timestamp

**Output**:
```
Task ID 1 marked as completed!
```

**Error Handling**:
- Task ID not found → Display: `Error: Task with ID {id} not found.`
- Already completed → Display: `Task ID {id} is already completed.`

---

#### 3.2.8 `uncomplete <id>`
**Usage**: `uncomplete 1`

**Behavior**:
- Set `completed = False`
- Update `updated_at` timestamp

**Output**:
```
Task ID 1 marked as incomplete!
```

**Error Handling**:
- Task ID not found → Display: `Error: Task with ID {id} not found.`
- Already incomplete → Display: `Task ID {id} is already incomplete.`

---

#### 3.2.9 `exit`
**Usage**: `exit`

**Behavior**:
- Display farewell message
- Exit application

**Output**:
```
JazakAllah Khair for using SalaatFlow! May your deeds be accepted.
```

---

## 4. Application Flow

### 4.1 Startup
1. Display welcome banner
2. Show help message (same as `help` command)
3. Enter command loop

**Welcome Banner**:
```
========================================
  SalaatFlow - Prayer & Spiritual Tasks
  Phase I: Console Edition
========================================
```

### 4.2 Command Loop
```
1. Display prompt: "salaatflow> "
2. Read user input
3. Parse command and arguments
4. Execute command handler
5. Display result
6. Repeat until "exit" command
```

### 4.3 Error Handling
- **Invalid command** → `Error: Unknown command '{cmd}'. Type 'help' for available commands.`
- **Missing required argument** → `Error: Command '{cmd}' requires argument(s). Usage: {usage}`
- **Invalid argument type** → `Error: Invalid argument. Expected {type}.`

---

## 5. Acceptance Criteria

### 5.1 Test Session 1: Basic CRUD Operations

**Scenario**: Add multiple tasks, view list, mark complete, delete

```
salaatflow> add
Enter task title (required): Attend Fajr at Masjid Al-Huda
Enter description (optional): Wake up 30 minutes early
Select category:
  1. Farz
  2. Sunnah
  3. Nafl
  4. Deed
Enter choice (1-4): 1
Enter masjid name (optional): Masjid Al-Huda
Enter area name (optional): DHA Phase 5
Enter due date/time (optional, format: YYYY-MM-DD HH:MM): 2025-12-28 05:30

Task added successfully! (ID: 1)

salaatflow> add
Enter task title (required): Read Surah Yaseen after Fajr
Enter description (optional):
Select category:
  1. Farz
  2. Sunnah
  3. Nafl
  4. Deed
Enter choice (1-4): 2
Enter masjid name (optional):
Enter area name (optional):
Enter due date/time (optional, format: YYYY-MM-DD HH:MM):

Task added successfully! (ID: 2)

salaatflow> add
Enter task title (required): Give charity today
Enter description (optional): Donate to local food bank
Select category:
  1. Farz
  2. Sunnah
  3. Nafl
  4. Deed
Enter choice (1-4): 4
Enter masjid name (optional):
Enter area name (optional):
Enter due date/time (optional, format: YYYY-MM-DD HH:MM):

Task added successfully! (ID: 3)

salaatflow> list
ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
1  | [ ]    | Farz     | Attend Fajr at Masjid Al-Huda | Masjid Al-Huda   | DHA Phase 5  | 2025-12-28 05:30
2  | [ ]    | Sunnah   | Read Surah Yaseen after Fajr   | -                | -            | -
3  | [ ]    | Deed     | Give charity today             | -                | -            | -

Total: 3 tasks (0 completed, 3 pending)

salaatflow> complete 1
Task ID 1 marked as completed!

salaatflow> list
ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
1  | [✓]    | Farz     | Attend Fajr at Masjid Al-Huda | Masjid Al-Huda   | DHA Phase 5  | 2025-12-28 05:30
2  | [ ]    | Sunnah   | Read Surah Yaseen after Fajr   | -                | -            | -
3  | [ ]    | Deed     | Give charity today             | -                | -            | -

Total: 3 tasks (1 completed, 2 pending)

salaatflow> delete 2
Are you sure you want to delete this task?
  ID: 2
  Title: Read Surah Yaseen after Fajr
Confirm deletion? (y/n): y

Task deleted successfully!

salaatflow> list
ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
1  | [✓]    | Farz     | Attend Fajr at Masjid Al-Huda | Masjid Al-Huda   | DHA Phase 5  | 2025-12-28 05:30
3  | [ ]    | Deed     | Give charity today             | -                | -            | -

Total: 2 tasks (1 completed, 1 pending)
```

**Expected Outcome**: ✅ All operations succeed, task list reflects changes

---

### 5.2 Test Session 2: Filtering Tasks

**Scenario**: Filter by pending and completed status

```
salaatflow> list pending
ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
3  | [ ]    | Deed     | Give charity today             | -                | -            | -

Total: 1 task (0 completed, 1 pending)

salaatflow> list completed
ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
1  | [✓]    | Farz     | Attend Fajr at Masjid Al-Huda | Masjid Al-Huda   | DHA Phase 5  | 2025-12-28 05:30

Total: 1 task (1 completed, 0 pending)

salaatflow> list all
ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
1  | [✓]    | Farz     | Attend Fajr at Masjid Al-Huda | Masjid Al-Huda   | DHA Phase 5  | 2025-12-28 05:30
3  | [ ]    | Deed     | Give charity today             | -                | -            | -

Total: 2 tasks (1 completed, 1 pending)
```

**Expected Outcome**: ✅ Filters correctly show only matching tasks

---

### 5.3 Test Session 3: Update Task

**Scenario**: Update task description and category

```
salaatflow> view 3
Task ID: 3
Title: Give charity today
Description: Donate to local food bank
Category: Deed
Masjid: -
Area: -
Due Date/Time: -
Status: Pending
Created: 2025-12-27 10:15:00
Last Updated: 2025-12-27 10:15:00

salaatflow> update 3

Updating Task ID: 3

Current title: Give charity today
New title (press Enter to keep current):

Current description: Donate to local food bank
New description (press Enter to keep current): Donate $50 to Masjid Al-Noor

Current category: Deed
Select new category (press Enter to keep current):
  1. Farz
  2. Sunnah
  3. Nafl
  4. Deed
Enter choice (1-4) or press Enter:

Current masjid: -
New masjid (press Enter to keep current): Masjid Al-Noor

Current area: -
New area (press Enter to keep current): Gulshan-e-Iqbal

Current due date/time: -
New due date/time (format: YYYY-MM-DD HH:MM, press Enter to keep current): 2025-12-27 18:00

Task updated successfully!

salaatflow> view 3
Task ID: 3
Title: Give charity today
Description: Donate $50 to Masjid Al-Noor
Category: Deed
Masjid: Masjid Al-Noor
Area: Gulshan-e-Iqbal
Due Date/Time: 2025-12-27 18:00
Status: Pending
Created: 2025-12-27 10:15:00
Last Updated: 2025-12-27 10:20:00
```

**Expected Outcome**: ✅ Task updated with new values, updated_at timestamp changed

---

### 5.4 Test Session 4: Error Handling

**Scenario**: Invalid commands and missing tasks

```
salaatflow> invalid_command
Error: Unknown command 'invalid_command'. Type 'help' for available commands.

salaatflow> delete
Error: Command 'delete' requires argument(s). Usage: delete <id>

salaatflow> delete 999
Error: Task with ID 999 not found.

salaatflow> complete abc
Error: Invalid task ID. Please enter a number.

salaatflow> view 999
Error: Task with ID 999 not found.

salaatflow> list invalid_filter
Error: Invalid filter. Use: all, pending, or completed
```

**Expected Outcome**: ✅ Graceful error messages, application continues running

---

### 5.5 Test Session 5: Complete Workflow

**Scenario**: Typical daily usage pattern

```
salaatflow> add
Enter task title (required): Pray Dhuhr at office
Enter description (optional): Set reminder 10 min before
Select category:
  1. Farz
  2. Sunnah
  3. Nafl
  4. Deed
Enter choice (1-4): 1
Enter masjid name (optional):
Enter area name (optional): Clifton
Enter due date/time (optional, format: YYYY-MM-DD HH:MM): 2025-12-27 13:30

Task added successfully! (ID: 4)

salaatflow> add
Enter task title (required): Recite Ayat-ul-Kursi before sleep
Enter description (optional):
Select category:
  1. Farz
  2. Sunnah
  3. Nafl
  4. Deed
Enter choice (1-4): 2
Enter masjid name (optional):
Enter area name (optional):
Enter due date/time (optional, format: YYYY-MM-DD HH:MM): 2025-12-27 23:00

Task added successfully! (ID: 5)

salaatflow> list pending
ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
3  | [ ]    | Deed     | Give charity today             | Masjid Al-Noor   | Gulshan      | 2025-12-27 18:00
4  | [ ]    | Farz     | Pray Dhuhr at office           | -                | Clifton      | 2025-12-27 13:30
5  | [ ]    | Sunnah   | Recite Ayat-ul-Kursi           | -                | -            | 2025-12-27 23:00

Total: 3 tasks (0 completed, 3 pending)

salaatflow> complete 4
Task ID 4 marked as completed!

salaatflow> uncomplete 1
Task ID 1 marked as incomplete!

salaatflow> list
ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time
---|--------|----------|--------------------------------|------------------|--------------|------------------
1  | [ ]    | Farz     | Attend Fajr at Masjid Al-Huda | Masjid Al-Huda   | DHA Phase 5  | 2025-12-28 05:30
3  | [ ]    | Deed     | Give charity today             | Masjid Al-Noor   | Gulshan      | 2025-12-27 18:00
4  | [✓]    | Farz     | Pray Dhuhr at office           | -                | Clifton      | 2025-12-27 13:30
5  | [ ]    | Sunnah   | Recite Ayat-ul-Kursi           | -                | -            | 2025-12-27 23:00

Total: 4 tasks (1 completed, 3 pending)

salaatflow> exit
JazakAllah Khair for using SalaatFlow! May your deeds be accepted.
```

**Expected Outcome**: ✅ All operations work seamlessly in realistic usage

---

## 6. Technical Requirements

### 6.1 Python Version
- Python 3.11 or higher

### 6.2 Dependencies
- **Standard Library Only**: No external packages required
- Modules to use:
  - `datetime` for timestamps
  - `sys` for CLI input/output
  - `typing` for type hints (optional but recommended)

### 6.3 Code Structure

Recommended file structure:
```
phase1/
├── main.py              # Entry point, REPL loop
├── models.py            # Task data model (dict or dataclass)
├── storage.py           # In-memory storage manager
├── commands.py          # Command handlers (add, list, update, etc.)
├── validators.py        # Input validation functions
├── display.py           # Output formatting (tables, messages)
└── README.md            # Usage instructions
```

### 6.4 Code Quality Standards
- **Type Hints**: Use Python type hints for all functions
- **Docstrings**: All public functions must have docstrings
- **Error Handling**: Use try-except blocks for user input parsing
- **Constants**: Define category options, max lengths as constants
- **DRY Principle**: Avoid code duplication

### 6.5 Testing
- Manual testing using the 5 acceptance test sessions above
- Optional: Unit tests for validation functions (not required for Phase I)

---

## 7. Implementation Checklist

- [ ] Create project directory structure
- [ ] Implement Task data model (dict or dataclass)
- [ ] Implement in-memory storage (list + auto-increment ID)
- [ ] Implement `add` command with interactive prompts
- [ ] Implement `list` command with filtering
- [ ] Implement `view` command
- [ ] Implement `update` command
- [ ] Implement `delete` command with confirmation
- [ ] Implement `complete` and `uncomplete` commands
- [ ] Implement `help` command
- [ ] Implement `exit` command
- [ ] Implement REPL loop in main.py
- [ ] Add input validation for all fields
- [ ] Add error handling for invalid commands and IDs
- [ ] Format output tables for `list` command
- [ ] Test all 5 acceptance criteria sessions
- [ ] Create README.md with usage instructions

---

## 8. Future Evolution Notes

This Phase I design intentionally supports evolution to Phase II:
- Task dict structure → SQLModel schema
- In-memory list → PostgreSQL database
- CLI commands → REST API endpoints
- Category strings → Database enum or foreign key

**Do NOT implement** in Phase I:
- Database connections
- API endpoints
- Authentication
- Recurring task logic
- Masjid timetable lookup
- Reminders or notifications

---

## 9. References

- **Global Constitution**: `/specs/constitution.md`
- **Hackathon Requirements**: Evolution of Todo (5 phases)
- **Domain Model**: Prayer & Spiritual Tasks for Islamic use cases

---

**Specification Status**: ✅ Ready for Implementation
**Next Step**: Generate implementation plan (`/sp.plan`)
