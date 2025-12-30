# Phase III: MCP Tools Specification - REFINED

## Executive Summary

This specification defines the **complete implementation** of all MCP (Model Context Protocol) tools required by the SalaatFlow chatbot agent.

**CRITICAL REQUIREMENT:** All tools referenced by the agent MUST be fully implemented and registered. Any `TOOL_NOT_FOUND` error at runtime is considered a **BUG** and fails acceptance criteria.

## 1. Tool Name Alignment

### 1.1 Official Tool Registry

The following tools MUST be implemented with these EXACT names:

#### Task Management Tools
- `create_task` - Create a new spiritual task
- `list_tasks` - List user's tasks with optional filters
- `update_task` - Update an existing task
- `delete_task` - Delete a task
- `complete_task` - Mark a task as completed

#### Masjid Tools
- `list_masjids` - List masjids with optional area filter
- `get_masjid_details` - Get detailed information about a specific masjid
- `search_masjids` - Search masjids by name or area

#### Prayer Time Tools
- `get_prayer_times` - Get prayer times for a specific masjid or area
- `get_current_prayer` - Get the current/next prayer information

#### Hadith Tools
- `get_daily_hadith` - Get the daily hadith
- `get_random_hadith` - Get a random hadith from the database

### 1.2 Name Consistency Rules

**MANDATORY:**
- Tool names MUST match EXACTLY across:
  1. Agent configuration (`chatbot/agent/config.py`)
  2. MCP tool implementation (`chatbot/mcp_tools/*.py`)
  3. Tool registry (`chatbot/mcp_tools/registry.py`)
  4. Agent tool declarations

**FORBIDDEN:**
- ❌ Using `create_spiritual_task` in one place and `create_task` in another
- ❌ Aliasing without explicit documentation
- ❌ Dynamic tool name generation that could cause mismatches

**VERIFICATION:**
- All tool names MUST be defined as constants in `chatbot/mcp_tools/constants.py`
- No string literals for tool names except in the constants file

## 2. MCP Tool Implementation Requirements

### 2.1 Tool Structure

Each MCP tool MUST implement this interface:

```python
from typing import Dict, Any, Optional
from pydantic import BaseModel

class ToolResult(BaseModel):
    """Standard tool result format"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_message: Optional[str] = None

def tool_name(
    user_id: int,
    **kwargs
) -> ToolResult:
    """
    Tool implementation.

    Args:
        user_id: The authenticated user's ID
        **kwargs: Tool-specific parameters

    Returns:
        ToolResult with success/failure and data

    Raises:
        ToolExecutionError: For unrecoverable errors
    """
    pass
```

### 2.2 Detailed Tool Specifications

#### Tool: `create_task`

**Purpose:** Create a new spiritual task for the user

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED - Authenticated user ID
    "title": str,                # REQUIRED - Task title (1-200 chars)
    "description": str,          # OPTIONAL - Task description
    "priority": str,             # OPTIONAL - "low", "medium", "high" (default: "medium")
    "linked_prayer": str,        # OPTIONAL - "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"
    "due_datetime": str,         # OPTIONAL - ISO 8601 datetime string
    "recurrence": str,           # OPTIONAL - "daily", "weekly", "monthly"
    "category": str,             # OPTIONAL - "prayer", "quran", "dhikr", "charity", "learning", "other"
}
```

**Backend Mapping:**
```
POST /api/v1/tasks
Headers:
  - Content-Type: application/json
  - X-User-ID: {user_id}

Body: {
  "title": str,
  "description": str,
  "priority": str,
  "linked_prayer": str,
  "due_datetime": str,
  "recurrence": str,
  "category": str,
  "masjid_id": null  # Set by user preference or default
}
```

**Expected Output:**
```python
{
    "success": true,
    "data": {
        "task": {
            "id": 123,
            "title": "Read Quran after Fajr",
            "description": "Complete 1 page",
            "priority": "high",
            "linked_prayer": "Fajr",
            "created_at": "2025-12-30T...",
            "completed": false
        }
    },
    "error": null,
    "error_message": null
}
```

**Error Handling:**
- `401`: User not authenticated → `ToolResult(success=False, error="AUTH_REQUIRED")`
- `400`: Invalid parameters → `ToolResult(success=False, error="INVALID_PARAMS", error_message=...)`
- `500`: Server error → `ToolResult(success=False, error="SERVER_ERROR")`

---

#### Tool: `list_tasks`

**Purpose:** List user's tasks with optional filtering

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED - Authenticated user ID
    "status": str,               # OPTIONAL - "pending", "completed", "all" (default: "pending")
    "priority": str,             # OPTIONAL - "low", "medium", "high"
    "linked_prayer": str,        # OPTIONAL - Filter by prayer
    "category": str,             # OPTIONAL - Filter by category
    "limit": int,                # OPTIONAL - Max results (default: 50)
}
```

**Backend Mapping:**
```
GET /api/v1/tasks?user_id={user_id}&status={status}&priority={priority}&linked_prayer={linked_prayer}&category={category}&limit={limit}
Headers:
  - X-User-ID: {user_id}
```

**Expected Output:**
```python
{
    "success": true,
    "data": {
        "tasks": [
            {
                "id": 123,
                "title": "Read Quran after Fajr",
                "priority": "high",
                "linked_prayer": "Fajr",
                "completed": false,
                "created_at": "2025-12-30T..."
            },
            ...
        ],
        "count": 5
    },
    "error": null,
    "error_message": null
}
```

---

#### Tool: `update_task`

**Purpose:** Update an existing task

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED
    "task_id": int,              # REQUIRED - Task ID to update
    "title": str,                # OPTIONAL
    "description": str,          # OPTIONAL
    "priority": str,             # OPTIONAL
    "linked_prayer": str,        # OPTIONAL
    "due_datetime": str,         # OPTIONAL
}
```

**Backend Mapping:**
```
PUT /api/v1/tasks/{task_id}
Headers:
  - X-User-ID: {user_id}
Body: {updated fields}
```

---

#### Tool: `delete_task`

**Purpose:** Delete a task

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED
    "task_id": int,              # REQUIRED - Task ID to delete
}
```

**Backend Mapping:**
```
DELETE /api/v1/tasks/{task_id}
Headers:
  - X-User-ID: {user_id}
```

---

#### Tool: `complete_task`

**Purpose:** Mark a task as completed

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED
    "task_id": int,              # REQUIRED - Task ID to complete
}
```

**Backend Mapping:**
```
PATCH /api/v1/tasks/{task_id}/complete
Headers:
  - X-User-ID: {user_id}
```

---

#### Tool: `list_masjids`

**Purpose:** List masjids with optional area filter

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED (for logging, not auth)
    "area": str,                 # OPTIONAL - Area name filter
    "city": str,                 # OPTIONAL - City filter (default: "Karachi")
    "limit": int,                # OPTIONAL - Max results (default: 10)
}
```

**Backend Mapping:**
```
GET /api/v1/masjids?area={area}&city={city}&limit={limit}
```

**Expected Output:**
```python
{
    "success": true,
    "data": {
        "masjids": [
            {
                "id": 1,
                "name": "Masjid Al-Noor",
                "area_name": "North Nazimabad",
                "city": "Karachi",
                "fajr_time": "05:30",
                "dhuhr_time": "12:45",
                ...
            },
            ...
        ],
        "count": 10
    }
}
```

---

#### Tool: `get_masjid_details`

**Purpose:** Get detailed information about a specific masjid

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED
    "masjid_id": int,            # REQUIRED - Masjid ID
}
```

**Backend Mapping:**
```
GET /api/v1/masjids/{masjid_id}
```

---

#### Tool: `search_masjids`

**Purpose:** Search masjids by name or area

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED
    "query": str,                # REQUIRED - Search query
    "area": str,                 # OPTIONAL - Area filter
}
```

**Backend Mapping:**
```
GET /api/v1/masjids/search?q={query}&area={area}
```

---

#### Tool: `get_prayer_times`

**Purpose:** Get prayer times for a masjid or area

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED
    "masjid_id": int,            # OPTIONAL - Specific masjid
    "area": str,                 # OPTIONAL - Area name
}
```

**Backend Mapping:**
```
# If masjid_id provided:
GET /api/v1/masjids/{masjid_id}

# If area provided:
GET /api/v1/masjids?area={area}&limit=1
```

**Expected Output:**
```python
{
    "success": true,
    "data": {
        "masjid_name": "Masjid Al-Noor",
        "area": "North Nazimabad",
        "prayer_times": {
            "fajr": "05:30",
            "dhuhr": "12:45",
            "asr": "16:00",
            "maghrib": "18:15",
            "isha": "19:45"
        }
    }
}
```

---

#### Tool: `get_current_prayer`

**Purpose:** Get current/next prayer information

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED
    "masjid_id": int,            # OPTIONAL - Default to user's preferred masjid
}
```

**Backend Mapping:**
```
GET /api/v1/masjids/{masjid_id}/current-prayer
```

---

#### Tool: `get_daily_hadith`

**Purpose:** Get the daily hadith

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED
    "date": str,                 # OPTIONAL - ISO date (default: today)
}
```

**Backend Mapping:**
```
GET /api/v1/hadith/daily?date={date}
```

**Expected Output:**
```python
{
    "success": true,
    "data": {
        "hadith": {
            "id": 1,
            "text_english": "The best of you are those who...",
            "text_urdu": "تم میں سے بہترین...",
            "narrator": "Abu Hurairah",
            "source": "Bukhari",
            "date": "2025-12-30"
        }
    }
}
```

---

#### Tool: `get_random_hadith`

**Purpose:** Get a random hadith

**Input Parameters:**
```python
{
    "user_id": int,              # REQUIRED
}
```

**Backend Mapping:**
```
GET /api/v1/hadith/random
```

---

### 2.3 Authentication Handling

**MANDATORY RULES:**

1. **User ID Propagation:**
   - All tools MUST receive `user_id` as the first parameter
   - The chatbot router extracts `user_id` from the chat request
   - If `user_id` is `null` and tool requires auth → return `AUTH_REQUIRED` error

2. **Backend Authentication:**
   - Tools MUST pass user_id to backend via:
     - **Option A:** `X-User-ID` header (current implementation)
     - **Option B:** JWT token in `Authorization` header (future)

3. **Authentication Errors:**
   - If backend returns 401 → Tool returns `ToolResult(success=False, error="AUTH_REQUIRED")`
   - Agent must inform user to log in

### 2.4 Error Handling Requirements

**MANDATORY ERROR PROPAGATION:**

Each tool MUST handle these error scenarios:

1. **Network Errors:**
   ```python
   except requests.exceptions.ConnectionError:
       return ToolResult(
           success=False,
           error="NETWORK_ERROR",
           error_message="Unable to connect to backend service"
       )
   ```

2. **Timeout Errors:**
   ```python
   except requests.exceptions.Timeout:
       return ToolResult(
           success=False,
           error="TIMEOUT",
           error_message="Request timed out"
       )
   ```

3. **Backend HTTP Errors:**
   ```python
   if response.status_code == 400:
       return ToolResult(
           success=False,
           error="INVALID_REQUEST",
           error_message=response.json().get("detail", "Invalid request")
       )
   elif response.status_code == 401:
       return ToolResult(
           success=False,
           error="AUTH_REQUIRED",
           error_message="Authentication required"
       )
   elif response.status_code == 404:
       return ToolResult(
           success=False,
           error="NOT_FOUND",
           error_message="Resource not found"
       )
   elif response.status_code >= 500:
       return ToolResult(
           success=False,
           error="SERVER_ERROR",
           error_message="Backend service error"
       )
   ```

4. **Validation Errors:**
   ```python
   from pydantic import ValidationError
   try:
       validated_params = ToolParams(**params)
   except ValidationError as e:
       return ToolResult(
           success=False,
           error="VALIDATION_ERROR",
           error_message=str(e)
       )
   ```

**FORBIDDEN:**
- ❌ Silent failures (returning success=true when operation failed)
- ❌ Swallowing exceptions without logging
- ❌ Generic error messages ("something went wrong")

## 3. MCP Tool Module & Registry

### 3.1 File Structure

```
backend/chatbot/mcp_tools/
├── __init__.py                  # Package init, exports all tools
├── constants.py                 # Tool name constants
├── registry.py                  # Central tool registry
├── base.py                      # Base classes and utilities
├── exceptions.py                # Custom exceptions
├── tasks_tools.py               # Task management tools
├── masjid_tools.py              # Masjid-related tools
├── prayer_tools.py              # Prayer time tools
├── hadith_tools.py              # Hadith tools
└── __tests__/                   # Tool tests
    ├── test_tasks_tools.py
    ├── test_masjid_tools.py
    ├── test_prayer_tools.py
    └── test_hadith_tools.py
```

### 3.2 Constants Definition

**File:** `backend/chatbot/mcp_tools/constants.py`

```python
"""
MCP Tool Name Constants

CRITICAL: These are the ONLY valid tool names.
Any tool name used MUST be defined here.
"""

# Task Management Tools
TOOL_CREATE_TASK = "create_task"
TOOL_LIST_TASKS = "list_tasks"
TOOL_UPDATE_TASK = "update_task"
TOOL_DELETE_TASK = "delete_task"
TOOL_COMPLETE_TASK = "complete_task"

# Masjid Tools
TOOL_LIST_MASJIDS = "list_masjids"
TOOL_GET_MASJID_DETAILS = "get_masjid_details"
TOOL_SEARCH_MASJIDS = "search_masjids"

# Prayer Time Tools
TOOL_GET_PRAYER_TIMES = "get_prayer_times"
TOOL_GET_CURRENT_PRAYER = "get_current_prayer"

# Hadith Tools
TOOL_GET_DAILY_HADITH = "get_daily_hadith"
TOOL_GET_RANDOM_HADITH = "get_random_hadith"

# All valid tool names
ALL_TOOL_NAMES = {
    TOOL_CREATE_TASK,
    TOOL_LIST_TASKS,
    TOOL_UPDATE_TASK,
    TOOL_DELETE_TASK,
    TOOL_COMPLETE_TASK,
    TOOL_LIST_MASJIDS,
    TOOL_GET_MASJID_DETAILS,
    TOOL_SEARCH_MASJIDS,
    TOOL_GET_PRAYER_TIMES,
    TOOL_GET_CURRENT_PRAYER,
    TOOL_GET_DAILY_HADITH,
    TOOL_GET_RANDOM_HADITH,
}
```

### 3.3 Tool Registry

**File:** `backend/chatbot/mcp_tools/registry.py`

```python
"""
MCP Tool Registry

This module maintains the central registry of all available tools.
The registry maps tool names to their implementations.

CRITICAL: All tools MUST be registered here.
Any tool not registered will cause TOOL_NOT_FOUND errors.
"""

from typing import Dict, Callable, Any
import logging

from .constants import *
from .tasks_tools import (
    create_task,
    list_tasks,
    update_task,
    delete_task,
    complete_task,
)
from .masjid_tools import (
    list_masjids,
    get_masjid_details,
    search_masjids,
)
from .prayer_tools import (
    get_prayer_times,
    get_current_prayer,
)
from .hadith_tools import (
    get_daily_hadith,
    get_random_hadith,
)

logger = logging.getLogger(__name__)


class ToolRegistry:
    """Central registry for all MCP tools"""

    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._register_all_tools()

    def _register_all_tools(self):
        """Register all available tools"""

        # Task Management Tools
        self.register(TOOL_CREATE_TASK, create_task)
        self.register(TOOL_LIST_TASKS, list_tasks)
        self.register(TOOL_UPDATE_TASK, update_task)
        self.register(TOOL_DELETE_TASK, delete_task)
        self.register(TOOL_COMPLETE_TASK, complete_task)

        # Masjid Tools
        self.register(TOOL_LIST_MASJIDS, list_masjids)
        self.register(TOOL_GET_MASJID_DETAILS, get_masjid_details)
        self.register(TOOL_SEARCH_MASJIDS, search_masjids)

        # Prayer Time Tools
        self.register(TOOL_GET_PRAYER_TIMES, get_prayer_times)
        self.register(TOOL_GET_CURRENT_PRAYER, get_current_prayer)

        # Hadith Tools
        self.register(TOOL_GET_DAILY_HADITH, get_daily_hadith)
        self.register(TOOL_GET_RANDOM_HADITH, get_random_hadith)

        logger.info(f"✅ Registered {len(self._tools)} MCP tools")

    def register(self, name: str, func: Callable):
        """Register a tool"""
        if name in self._tools:
            logger.warning(f"Tool '{name}' already registered, overwriting")
        self._tools[name] = func
        logger.debug(f"Registered tool: {name}")

    def get(self, name: str) -> Callable:
        """Get a tool by name"""
        if name not in self._tools:
            raise KeyError(f"Tool not found: {name}")
        return self._tools[name]

    def has(self, name: str) -> bool:
        """Check if a tool is registered"""
        return name in self._tools

    def list_tools(self) -> list[str]:
        """List all registered tool names"""
        return list(self._tools.keys())


# Global registry instance
_registry = ToolRegistry()


def get_tool_registry() -> ToolRegistry:
    """Get the global tool registry"""
    return _registry


def execute_tool(tool_name: str, user_id: int, **kwargs) -> Dict[str, Any]:
    """
    Execute a tool by name.

    Args:
        tool_name: Name of the tool to execute
        user_id: User ID for authentication
        **kwargs: Tool-specific parameters

    Returns:
        Tool execution result

    Raises:
        KeyError: If tool not found (this should NEVER happen in production)
    """
    registry = get_tool_registry()

    if not registry.has(tool_name):
        logger.error(
            f"TOOL_NOT_FOUND: '{tool_name}' is not registered. "
            f"Available tools: {registry.list_tools()}"
        )
        return {
            "success": False,
            "error": "TOOL_NOT_FOUND",
            "error_message": f"Tool '{tool_name}' is not implemented or registered",
            "available_tools": registry.list_tools()
        }

    try:
        tool_func = registry.get(tool_name)
        result = tool_func(user_id=user_id, **kwargs)

        # Convert ToolResult to dict if needed
        if hasattr(result, 'dict'):
            return result.dict()
        return result

    except Exception as e:
        logger.error(
            f"Error executing tool '{tool_name}': {e}",
            exc_info=True
        )
        return {
            "success": False,
            "error": "TOOL_EXECUTION_ERROR",
            "error_message": str(e)
        }
```

### 3.4 Tool Base Classes

**File:** `backend/chatbot/mcp_tools/base.py`

```python
"""
Base classes and utilities for MCP tools
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
import os


class ToolResult(BaseModel):
    """Standard tool result format"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_message: Optional[str] = None


class BackendClient:
    """Base client for making backend HTTP requests"""

    def __init__(self):
        self.base_url = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")
        self.timeout = 10

    def _get_headers(self, user_id: int) -> Dict[str, str]:
        """Get headers for backend requests"""
        return {
            "Content-Type": "application/json",
            "X-User-ID": str(user_id),
        }

    def _handle_response(self, response) -> ToolResult:
        """Handle HTTP response and convert to ToolResult"""
        import requests

        try:
            response.raise_for_status()
            data = response.json()
            return ToolResult(success=True, data=data)

        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                return ToolResult(
                    success=False,
                    error="AUTH_REQUIRED",
                    error_message="Authentication required"
                )
            elif response.status_code == 404:
                return ToolResult(
                    success=False,
                    error="NOT_FOUND",
                    error_message="Resource not found"
                )
            elif response.status_code >= 500:
                return ToolResult(
                    success=False,
                    error="SERVER_ERROR",
                    error_message="Backend service error"
                )
            else:
                error_data = response.json() if response.text else {}
                return ToolResult(
                    success=False,
                    error="HTTP_ERROR",
                    error_message=error_data.get("detail", str(e))
                )
```

## 4. Agent + MCP Integration

### 4.1 Agent Configuration

**File:** `backend/chatbot/agent/config.py`

Must be updated to declare all tools:

```python
"""
Agent Configuration

Defines which tools the agent can use.
"""

from chatbot.mcp_tools.constants import *

# Tools available to the agent
AGENT_TOOLS = [
    # Task Management
    TOOL_CREATE_TASK,
    TOOL_LIST_TASKS,
    TOOL_UPDATE_TASK,
    TOOL_DELETE_TASK,
    TOOL_COMPLETE_TASK,

    # Masjid
    TOOL_LIST_MASJIDS,
    TOOL_GET_MASJID_DETAILS,
    TOOL_SEARCH_MASJIDS,

    # Prayer Times
    TOOL_GET_PRAYER_TIMES,
    TOOL_GET_CURRENT_PRAYER,

    # Hadith
    TOOL_GET_DAILY_HADITH,
    TOOL_GET_RANDOM_HADITH,
]

# Verify all tools are valid
from chatbot.mcp_tools.constants import ALL_TOOL_NAMES

assert set(AGENT_TOOLS).issubset(ALL_TOOL_NAMES), \
    f"Invalid tool names in AGENT_TOOLS: {set(AGENT_TOOLS) - ALL_TOOL_NAMES}"
```

### 4.2 Agent Runtime Integration

**File:** `backend/chatbot/agent/agent.py`

Must use the tool registry:

```python
from chatbot.mcp_tools.registry import execute_tool

def run_agent(...):
    # ... intent detection ...

    if intent == "create_task":
        # Call the tool via registry
        result = execute_tool(
            "create_task",  # This MUST match constants.TOOL_CREATE_TASK
            user_id=user_id,
            title=params.get('title'),
            description=user_message,
            priority=params.get('priority', 'medium'),
            linked_prayer=params.get('linked_prayer')
        )

        # TOOL_NOT_FOUND is now a BUG
        if result.get('error') == 'TOOL_NOT_FOUND':
            logger.critical(
                f"CRITICAL BUG: Tool 'create_task' not found! "
                f"This should never happen in production."
            )
            # ... error handling ...
```

### 4.3 Startup Validation

**File:** `backend/main.py`

Must validate all tools on startup:

```python
from chatbot.mcp_tools.registry import get_tool_registry
from chatbot.agent.config import AGENT_TOOLS
import logging

logger = logging.getLogger(__name__)

@app.on_event("startup")
async def validate_mcp_tools():
    """Validate that all agent tools are registered"""
    registry = get_tool_registry()

    missing_tools = []
    for tool_name in AGENT_TOOLS:
        if not registry.has(tool_name):
            missing_tools.append(tool_name)

    if missing_tools:
        error_msg = (
            f"CRITICAL: The following tools are declared in AGENT_TOOLS "
            f"but not registered: {missing_tools}. "
            f"This will cause TOOL_NOT_FOUND errors at runtime."
        )
        logger.critical(error_msg)
        raise RuntimeError(error_msg)

    logger.info(
        f"✅ All {len(AGENT_TOOLS)} agent tools are registered and ready"
    )
```

## 5. Removal of "Expected TOOL_NOT_FOUND" Behavior

### 5.1 Previous Behavior (DEPRECATED)

The following statements are **NO LONGER VALID**:

> ❌ "The `TOOL_NOT_FOUND` error means the MCP tools are not implemented yet. This is expected."

> ❌ "The chatbot is working correctly, but the task management tools need to be set up."

> ❌ "MCP tools return TOOL_NOT_FOUND (expected - not implemented yet)"

### 5.2 New Behavior (MANDATORY)

**For Phase III completion:**

✅ **All tools referenced by the agent MUST exist and be functional**

✅ **Any `TOOL_NOT_FOUND` at runtime is a BUG and fails acceptance criteria**

✅ **The system MUST validate tool registration on startup**

✅ **Tool implementation status is NOT "expected to be missing"**

### 5.3 Error Classification

| Error | Status | Action |
|-------|--------|--------|
| `TOOL_NOT_FOUND` | **BUG** | Fix immediately - tool must be implemented and registered |
| `AUTH_REQUIRED` | Expected | User needs to log in |
| `VALIDATION_ERROR` | Expected | Invalid parameters |
| `SERVER_ERROR` | Expected | Backend service issue |
| `NETWORK_ERROR` | Expected | Connectivity issue |

## 6. Acceptance Criteria

### 6.1 Core Acceptance Tests

For Phase III to be considered **COMPLETE**, the following tests MUST pass:

#### Test 1: Create Task Flow
```python
def test_create_task_flow():
    """
    User: "Fajr ka task bana do"
    Expected:
    1. Agent detects create_task intent
    2. Calls execute_tool("create_task", user_id=1, ...)
    3. Tool calls POST /api/v1/tasks
    4. Task is created in database
    5. User sees success message
    6. NO TOOL_NOT_FOUND error
    """
    response = chat("Fajr ka task bana do", user_id=1)

    assert response["success"] == True
    assert "TOOL_NOT_FOUND" not in response["message"]
    assert "task" in response.get("data", {})

    # Verify task exists in database
    tasks = requests.get(f"{API_URL}/tasks?user_id=1").json()
    assert len(tasks) > 0
    assert any("Fajr" in t["title"] for t in tasks)
```

#### Test 2: List Tasks Flow
```python
def test_list_tasks_flow():
    """
    User: "Mujhe mere tasks dikhao"
    Expected:
    1. Agent detects list_tasks intent
    2. Calls execute_tool("list_tasks", user_id=1)
    3. Tool calls GET /api/v1/tasks
    4. Tasks are retrieved from database
    5. User sees task list
    6. NO TOOL_NOT_FOUND error
    """
    response = chat("Mujhe mere tasks dikhao", user_id=1)

    assert response["success"] == True
    assert "TOOL_NOT_FOUND" not in response["message"]
    assert "tasks" in response.get("data", {}) or "task" in response["message"].lower()
```

#### Test 3: Complete Task Flow
```python
def test_complete_task_flow():
    """
    User: "Task 123 complete karo"
    Expected:
    1. Agent detects complete_task intent
    2. Extracts task_id=123
    3. Calls execute_tool("complete_task", user_id=1, task_id=123)
    4. Tool calls PATCH /api/v1/tasks/123/complete
    5. Task is marked completed in database
    6. User sees success confirmation
    7. NO TOOL_NOT_FOUND error
    """
    response = chat("Task 123 complete karo", user_id=1)

    assert response["success"] == True
    assert "TOOL_NOT_FOUND" not in response["message"]
```

#### Test 4: List Masjids Flow
```python
def test_list_masjids_flow():
    """
    User: "North Nazimabad mein konsi masjid hai?"
    Expected:
    1. Agent detects search_masjids intent
    2. Extracts area="North Nazimabad"
    3. Calls execute_tool("search_masjids", area="North Nazimabad")
    4. Tool calls GET /api/v1/masjids?area=North+Nazimabad
    5. Masjids are retrieved
    6. User sees masjid list
    7. NO TOOL_NOT_FOUND error
    """
    response = chat("North Nazimabad mein konsi masjid hai?", user_id=None)

    assert response["success"] == True
    assert "TOOL_NOT_FOUND" not in response["message"]
    assert "masjid" in response["message"].lower()
```

#### Test 5: Get Prayer Times Flow
```python
def test_prayer_times_flow():
    """
    User: "Namaz ka time kya hai?"
    Expected:
    1. Agent detects get_prayer_times intent
    2. Calls execute_tool("get_prayer_times", user_id=1)
    3. Tool calls GET /api/v1/masjids/{default_masjid}
    4. Prayer times are retrieved
    5. User sees prayer schedule
    6. NO TOOL_NOT_FOUND error
    """
    response = chat("Namaz ka time kya hai?", user_id=1)

    assert response["success"] == True
    assert "TOOL_NOT_FOUND" not in response["message"]
    assert any(prayer in response["message"].lower()
               for prayer in ["fajr", "dhuhr", "asr", "maghrib", "isha"])
```

#### Test 6: Get Daily Hadith Flow
```python
def test_daily_hadith_flow():
    """
    User: "Aaj ki hadith sunao"
    Expected:
    1. Agent detects get_daily_hadith intent
    2. Calls execute_tool("get_daily_hadith", user_id=1)
    3. Tool calls GET /api/v1/hadith/daily
    4. Hadith is retrieved
    5. User sees hadith text
    6. NO TOOL_NOT_FOUND error
    """
    response = chat("Aaj ki hadith sunao", user_id=1)

    assert response["success"] == True
    assert "TOOL_NOT_FOUND" not in response["message"]
    assert "hadith" in response["message"].lower()
```

### 6.2 Startup Validation Test

```python
def test_startup_validation():
    """
    Test that the application validates tool registration on startup
    """
    # This should NOT raise an exception
    # If any tool is missing, startup MUST fail

    from main import validate_mcp_tools
    validate_mcp_tools()  # Should not raise
```

### 6.3 Tool Registry Test

```python
def test_all_tools_registered():
    """
    Verify that ALL tools declared in AGENT_TOOLS are registered
    """
    from chatbot.mcp_tools.registry import get_tool_registry
    from chatbot.agent.config import AGENT_TOOLS

    registry = get_tool_registry()

    for tool_name in AGENT_TOOLS:
        assert registry.has(tool_name), \
            f"Tool '{tool_name}' is declared but not registered"
```

### 6.4 No TOOL_NOT_FOUND Test

```python
def test_no_tool_not_found_in_responses():
    """
    Test common conversation flows to ensure NO TOOL_NOT_FOUND errors
    """
    test_cases = [
        ("Create a Fajr task", 1),
        ("Show my tasks", 1),
        ("Delete task 1", 1),
        ("Find masjids in DHA", None),
        ("What time is Maghrib?", 1),
        ("Tell me today's hadith", 1),
    ]

    for message, user_id in test_cases:
        response = chat(message, user_id=user_id)

        # CRITICAL: No TOOL_NOT_FOUND allowed
        assert "TOOL_NOT_FOUND" not in str(response), \
            f"TOOL_NOT_FOUND error for: '{message}'"
```

## 7. Documentation Requirements

### 7.1 Primary Specification Document

**File:** `docs/phase3_spec.md`

Must include:

1. **Tool Name Reference Table:**
   ```markdown
   | Tool Name | Purpose | Auth Required | Backend Endpoint |
   |-----------|---------|---------------|------------------|
   | create_task | Create spiritual task | Yes | POST /api/v1/tasks |
   | list_tasks | List user tasks | Yes | GET /api/v1/tasks |
   | ... | ... | ... | ... |
   ```

2. **Tool Input/Output Schemas:**
   - For each tool, document exact parameters and return format

3. **Error Handling:**
   - List all possible error codes
   - Describe user-facing error messages

### 7.2 MCP Tools Developer Guide

**File:** `docs/phase3_mcp_tools.md`

Must include:

1. **Adding a New Tool:**
   ```markdown
   ## How to Add a New Tool

   1. Add tool name constant to `mcp_tools/constants.py`
   2. Implement tool in appropriate module (e.g., `tasks_tools.py`)
   3. Register tool in `mcp_tools/registry.py`
   4. Add tool name to `agent/config.py` AGENT_TOOLS
   5. Write tests in `mcp_tools/__tests__/`
   6. Restart application - startup validation will verify registration
   ```

2. **Tool Implementation Template:**
   ```python
   from .base import ToolResult, BackendClient
   import requests

   def my_new_tool(user_id: int, **kwargs) -> ToolResult:
       """
       Description of what this tool does.

       Args:
           user_id: Authenticated user ID
           param1: Description

       Returns:
           ToolResult with success/failure
       """
       client = BackendClient()

       try:
           response = requests.post(
               f"{client.base_url}/api/v1/endpoint",
               json=kwargs,
               headers=client._get_headers(user_id),
               timeout=client.timeout
           )
           return client._handle_response(response)

       except requests.exceptions.RequestException as e:
           return ToolResult(
               success=False,
               error="NETWORK_ERROR",
               error_message=str(e)
           )
   ```

3. **Troubleshooting TOOL_NOT_FOUND:**
   ```markdown
   ## If You Get TOOL_NOT_FOUND

   This error means a tool is used but not registered. To fix:

   1. Check `chatbot/mcp_tools/constants.py` - is the tool name defined?
   2. Check `chatbot/mcp_tools/registry.py` - is the tool registered?
   3. Check the implementation file - does the function exist?
   4. Check `chatbot/agent/config.py` - is the tool listed in AGENT_TOOLS?
   5. Restart the server - startup validation will catch the issue
   ```

### 7.3 Main README Update

**File:** `README.md`

Must include:

```markdown
## Phase III: AI-Powered Chatbot ✅

The SalaatFlow chatbot is fully functional with complete MCP tool integration:

### Features
- ✅ Create, list, update, delete spiritual tasks via chat
- ✅ Find masjids and get prayer times via chat
- ✅ Get daily hadith via chat
- ✅ Bilingual support (English & Urdu)
- ✅ Context-aware conversations
- ✅ Robust error handling

### MCP Tools
All chatbot tools are implemented and registered. The system validates tool availability on startup.

**No TOOL_NOT_FOUND errors should occur in a correctly configured system.**

See `docs/phase3_mcp_tools.md` for developer documentation.
```

## 8. Implementation Checklist

### 8.1 Pre-Implementation Validation

- [ ] All tool names defined in `constants.py`
- [ ] Tool name constants used (no string literals)
- [ ] Backend API endpoints exist and are tested
- [ ] Authentication mechanism is clear

### 8.2 Implementation Steps

- [ ] Create `mcp_tools/` directory structure
- [ ] Implement `constants.py` with all tool names
- [ ] Implement `base.py` with ToolResult and BackendClient
- [ ] Implement `exceptions.py` with custom exceptions
- [ ] Implement `tasks_tools.py` with all task tools
- [ ] Implement `masjid_tools.py` with all masjid tools
- [ ] Implement `prayer_tools.py` with all prayer tools
- [ ] Implement `hadith_tools.py` with all hadith tools
- [ ] Implement `registry.py` with tool registration
- [ ] Update `agent/config.py` to declare tools
- [ ] Update `agent/agent.py` to use execute_tool
- [ ] Add startup validation to `main.py`
- [ ] Write unit tests for each tool
- [ ] Write integration tests for flows

### 8.3 Testing & Validation

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All acceptance criteria tests pass
- [ ] Startup validation passes
- [ ] No TOOL_NOT_FOUND in any test scenario
- [ ] Manual testing of all conversation flows

### 8.4 Documentation

- [ ] Update `docs/phase3_spec.md` with tool reference
- [ ] Create `docs/phase3_mcp_tools.md` developer guide
- [ ] Update `README.md` with Phase III status
- [ ] Add inline code documentation
- [ ] Update API documentation

## 9. Constraints & Requirements

### 9.1 Mandatory Requirements

1. **Tool Registration:**
   - ALL tools MUST be registered in the registry
   - Registration MUST happen before agent initialization
   - Startup validation MUST verify all tools exist

2. **Naming Consistency:**
   - Tool names MUST be defined as constants
   - Same constant MUST be used everywhere
   - No string literal tool names except in constants.py

3. **Error Handling:**
   - All network errors MUST be caught and converted to ToolResult
   - All HTTP errors MUST be classified and reported
   - No silent failures allowed

4. **Testing:**
   - Each tool MUST have unit tests
   - Each conversation flow MUST have integration tests
   - NO TOOL_NOT_FOUND in any test

### 9.2 Forbidden Patterns

❌ **FORBIDDEN:**
- Using tool name string literals outside constants.py
- Catching exceptions without logging
- Returning success=true when operation failed
- Allowing TOOL_NOT_FOUND in production
- Skipping startup validation

### 9.3 Implementation Method

✅ **ALLOWED:**
- AI code generation for all implementation
- Automated testing
- CI/CD validation

❌ **NOT ALLOWED:**
- Manual coding by humans (all via AI)
- Skipping tests
- Disabling startup validation

## 10. Success Criteria

Phase III is considered **COMPLETE** when:

1. ✅ All 12 tools are implemented and registered
2. ✅ Startup validation passes (no missing tools)
3. ✅ All unit tests pass
4. ✅ All integration tests pass
5. ✅ All acceptance criteria tests pass
6. ✅ NO TOOL_NOT_FOUND errors in any scenario
7. ✅ All documentation is updated
8. ✅ Manual testing confirms all flows work
9. ✅ Error handling is robust and tested
10. ✅ Code follows the specification exactly

## Appendix A: Tool Reference Quick Guide

| Tool | Intent Keywords | Auth | Backend Endpoint |
|------|----------------|------|------------------|
| `create_task` | "create", "bana", "add" + "task" | Required | POST /tasks |
| `list_tasks` | "show", "list", "dikhao" + "task" | Required | GET /tasks |
| `update_task` | "update", "change", "edit" + "task" | Required | PUT /tasks/{id} |
| `delete_task` | "delete", "remove", "hata" + "task" | Required | DELETE /tasks/{id} |
| `complete_task` | "complete", "done", "finish" + "task" | Required | PATCH /tasks/{id}/complete |
| `list_masjids` | "masjid", "mosque" + area | Optional | GET /masjids |
| `get_masjid_details` | "details", "info" + masjid name | Optional | GET /masjids/{id} |
| `search_masjids` | "search", "find" + "masjid" | Optional | GET /masjids/search |
| `get_prayer_times` | "prayer time", "namaz time" | Optional | GET /masjids/{id} |
| `get_current_prayer` | "current prayer", "next prayer" | Optional | GET /masjids/{id}/current-prayer |
| `get_daily_hadith` | "daily hadith", "aaj ki hadith" | Optional | GET /hadith/daily |
| `get_random_hadith` | "random hadith", "koi hadith" | Optional | GET /hadith/random |

## Appendix B: Conversation Examples

### Example 1: Create Task
```
User: "Fajr ke baad Quran parhne ka task bana do"

1. Agent detects: create_task
2. Extracts: title="Quran parhna", linked_prayer="Fajr"
3. Calls: execute_tool("create_task", user_id=1, title="Quran parhna", linked_prayer="Fajr")
4. Tool makes: POST /api/v1/tasks
5. Backend creates task in DB
6. Tool returns: ToolResult(success=True, data={task})
7. Agent responds: "✅ Task created successfully! Quran parhna (Fajr)"
```

### Example 2: List Tasks
```
User: "Mere pending tasks dikhao"

1. Agent detects: list_tasks
2. Extracts: status="pending"
3. Calls: execute_tool("list_tasks", user_id=1, status="pending")
4. Tool makes: GET /api/v1/tasks?status=pending&user_id=1
5. Backend retrieves tasks from DB
6. Tool returns: ToolResult(success=True, data={tasks: [...]})
7. Agent responds: "📋 Your pending tasks: 1. Quran parhna (Fajr) ..."
```

---

**END OF SPECIFICATION**

**Version:** 2.0 (Refined)
**Date:** 2025-12-30
**Status:** Ready for Implementation
**Critical Change:** TOOL_NOT_FOUND is now a BUG, not an expected state
