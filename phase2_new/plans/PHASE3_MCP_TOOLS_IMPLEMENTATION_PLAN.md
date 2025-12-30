# Phase III: MCP Tools Implementation Plan

## Executive Summary

**Objective:** Eliminate all `TOOL_NOT_FOUND` errors by implementing and registering all MCP tools required by the SalaatFlow chatbot agent.

**Current State:** Agent is configured to call MCP tools, but they return `TOOL_NOT_FOUND` at runtime.

**Target State:** All 12 MCP tools fully implemented, registered, tested, and working in conversation flows.

**Success Criteria:** ZERO `TOOL_NOT_FOUND` errors in any conversation scenario.

---

## Milestone 1: Tool Name Discovery & Alignment

### Objective
Discover the exact tool names currently used by the agent and align them with the specification.

### Tasks

#### 1.1 Inspect Agent Configuration
**Files to examine:**
- `backend/chatbot/agent/agent.py` - Main agent logic
- `backend/chatbot/agent/config.py` - Agent configuration
- `backend/chatbot/agent/prompts.py` - System prompts
- `backend/chatbot/mcp_tools.py` - Current tool stub (if exists)

**Actions:**
```bash
# Search for tool names in agent code
cd backend
grep -r "create_task\|list_tasks\|update_task\|delete_task" chatbot/agent/
grep -r "list_masjids\|search_masjids\|get_masjid" chatbot/agent/
grep -r "get_prayer_times\|get_hadith" chatbot/agent/
```

**Expected findings:**
- List of tool names currently referenced
- Intent detection patterns (e.g., "create" + "task" → `create_task`)
- Current tool execution mechanism (e.g., `execute_tool(name, **params)`)

#### 1.2 Extract Current Tool List

**Create inventory document:**

`backend/chatbot/CURRENT_TOOL_INVENTORY.md`:
```markdown
# Current Tool Usage Inventory

## Tools Called by Agent

| Tool Name | Called From | Current Status | Spec Name | Action |
|-----------|-------------|----------------|-----------|--------|
| create_task | agent.py:210 | NOT_IMPLEMENTED | create_task | Implement |
| list_tasks | agent.py:235 | NOT_IMPLEMENTED | list_tasks | Implement |
| update_task | (not called) | NOT_IMPLEMENTED | update_task | Implement |
| delete_task | (not called) | NOT_IMPLEMENTED | delete_task | Implement |
| complete_task | (not called) | NOT_IMPLEMENTED | complete_task | Implement |
| search_masjids | agent.py:268 | NOT_IMPLEMENTED | search_masjids | Implement |
| ... | ... | ... | ... | ... |
```

#### 1.3 Compare with Specification

**Actions:**
1. Read `docs/PHASE3_MCP_TOOLS_SPECIFICATION.md` section 1.1
2. Compare agent's tool list with spec's canonical list
3. Identify:
   - ✅ Tools that match exactly
   - ⚠️ Tools with naming mismatches (e.g., `get_masjid` vs `get_masjid_details`)
   - ❌ Tools in spec but not called by agent
   - ⚠️ Tools called by agent but not in spec

**Create alignment document:**

`backend/chatbot/TOOL_NAME_ALIGNMENT.md`:
```markdown
# Tool Name Alignment

## Perfect Matches (Implement As-Is)
- create_task ✅
- list_tasks ✅
- search_masjids ✅

## Naming Mismatches (Requires Renaming)
- Agent calls: `get_masjid(id)` → Spec: `get_masjid_details(masjid_id)`
  - Action: Update agent to call `get_masjid_details`

## Missing from Agent (Implement but Low Priority)
- update_task - Not currently called, but should be available
- delete_task - Not currently called, but should be available

## Agent-Only (Not in Spec)
- (None expected)
```

### Deliverables
- ✅ `CURRENT_TOOL_INVENTORY.md` - Complete tool usage inventory
- ✅ `TOOL_NAME_ALIGNMENT.md` - Alignment plan
- ✅ List of exact tool names to implement (should be 12 as per spec)

### Validation
```bash
# Count tools to implement
grep "Implement" CURRENT_TOOL_INVENTORY.md | wc -l
# Should output: 12
```

---

## Milestone 2: MCP Tool Module Creation

### Objective
Implement all 12 MCP tools with proper HTTP backend integration.

### 2.1 Foundation Files

#### Create Base Infrastructure

**File:** `backend/chatbot/mcp_tools/__init__.py`
```python
"""
MCP Tools Package

Provides all tools available to the chatbot agent.
"""

from .registry import get_tool_registry, execute_tool
from .constants import *

__all__ = [
    "get_tool_registry",
    "execute_tool",
]
```

**File:** `backend/chatbot/mcp_tools/constants.py`
```python
"""
MCP Tool Name Constants

CRITICAL: These are the ONLY valid tool names.
All tool references MUST use these constants.
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

**File:** `backend/chatbot/mcp_tools/base.py`
```python
"""
Base classes and utilities for MCP tools
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
import os
import requests
import logging

logger = logging.getLogger(__name__)


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

    def _handle_response(self, response: requests.Response) -> ToolResult:
        """Handle HTTP response and convert to ToolResult"""
        try:
            response.raise_for_status()
            data = response.json()
            return ToolResult(success=True, data=data)

        except requests.exceptions.HTTPError:
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
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", response.text)
                except:
                    error_msg = response.text

                return ToolResult(
                    success=False,
                    error="HTTP_ERROR",
                    error_message=error_msg
                )

        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            return ToolResult(
                success=False,
                error="NETWORK_ERROR",
                error_message="Unable to connect to backend"
            )

        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout error: {e}")
            return ToolResult(
                success=False,
                error="TIMEOUT",
                error_message="Request timed out"
            )

        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return ToolResult(
                success=False,
                error="UNKNOWN_ERROR",
                error_message=str(e)
            )
```

**File:** `backend/chatbot/mcp_tools/exceptions.py`
```python
"""
Custom exceptions for MCP tools
"""


class ToolExecutionError(Exception):
    """Base exception for tool execution errors"""
    pass


class ToolNotFoundError(ToolExecutionError):
    """Raised when a tool is not found in the registry"""
    pass


class ToolValidationError(ToolExecutionError):
    """Raised when tool parameters are invalid"""
    pass
```

### 2.2 Task Management Tools

**File:** `backend/chatbot/mcp_tools/tasks_tools.py`

**Implementation checklist:**
- [ ] `create_task(user_id, title, description, priority, linked_prayer, ...)`
  - POST to `/api/v1/tasks`
  - Validate parameters
  - Return task data or error
- [ ] `list_tasks(user_id, status, priority, linked_prayer, limit)`
  - GET from `/api/v1/tasks` with query params
  - Return list of tasks
- [ ] `update_task(user_id, task_id, **updates)`
  - PUT to `/api/v1/tasks/{task_id}`
  - Return updated task
- [ ] `delete_task(user_id, task_id)`
  - DELETE to `/api/v1/tasks/{task_id}`
  - Return success confirmation
- [ ] `complete_task(user_id, task_id)`
  - PATCH to `/api/v1/tasks/{task_id}/complete`
  - Return completed task

**Template for each tool:**
```python
from .base import ToolResult, BackendClient
from .constants import TOOL_CREATE_TASK
import requests
import logging

logger = logging.getLogger(__name__)


def create_task(
    user_id: int,
    title: str,
    description: str = "",
    priority: str = "medium",
    linked_prayer: str = None,
    **kwargs
) -> ToolResult:
    """
    Create a new spiritual task.

    Args:
        user_id: User ID (required for auth)
        title: Task title (required)
        description: Task description
        priority: Task priority (low, medium, high)
        linked_prayer: Linked prayer (Fajr, Dhuhr, Asr, Maghrib, Isha)
        **kwargs: Additional parameters

    Returns:
        ToolResult with task data or error
    """
    client = BackendClient()

    # Build request payload
    payload = {
        "title": title,
        "description": description,
        "priority": priority,
        "user_id": user_id,
    }

    if linked_prayer:
        payload["linked_prayer"] = linked_prayer

    # Add optional fields from kwargs
    for key in ["due_datetime", "recurrence", "category", "masjid_id"]:
        if key in kwargs:
            payload[key] = kwargs[key]

    try:
        logger.debug(f"Creating task: {payload}")

        response = requests.post(
            f"{client.base_url}/api/v1/tasks",
            json=payload,
            headers=client._get_headers(user_id),
            timeout=client.timeout
        )

        result = client._handle_response(response)

        if result.success:
            logger.info(f"Task created successfully: {result.data.get('id')}")

        return result

    except Exception as e:
        logger.error(f"Error creating task: {e}", exc_info=True)
        return ToolResult(
            success=False,
            error="TOOL_EXECUTION_ERROR",
            error_message=str(e)
        )
```

### 2.3 Masjid Tools

**File:** `backend/chatbot/mcp_tools/masjid_tools.py`

**Implementation checklist:**
- [ ] `list_masjids(user_id, area, city, limit)`
  - GET from `/api/v1/masjids` with filters
- [ ] `get_masjid_details(user_id, masjid_id)`
  - GET from `/api/v1/masjids/{masjid_id}`
- [ ] `search_masjids(user_id, query, area)`
  - GET from `/api/v1/masjids/search?q={query}`

### 2.4 Prayer Time Tools

**File:** `backend/chatbot/mcp_tools/prayer_tools.py`

**Implementation checklist:**
- [ ] `get_prayer_times(user_id, masjid_id, area)`
  - GET masjid data and extract prayer times
- [ ] `get_current_prayer(user_id, masjid_id)`
  - GET current/next prayer based on time

### 2.5 Hadith Tools

**File:** `backend/chatbot/mcp_tools/hadith_tools.py`

**Implementation checklist:**
- [ ] `get_daily_hadith(user_id, date)`
  - GET from `/api/v1/hadith/daily`
- [ ] `get_random_hadith(user_id)`
  - GET from `/api/v1/hadith/random`

### Deliverables
- ✅ All 12 tool functions implemented
- ✅ All tools use BackendClient for HTTP calls
- ✅ All tools return ToolResult
- ✅ All tools handle errors properly

### Validation
```bash
# Check all tools are implemented
ls -la backend/chatbot/mcp_tools/*.py

# Count functions in each file
grep "^def " backend/chatbot/mcp_tools/tasks_tools.py | wc -l  # Should be 5
grep "^def " backend/chatbot/mcp_tools/masjid_tools.py | wc -l  # Should be 3
grep "^def " backend/chatbot/mcp_tools/prayer_tools.py | wc -l  # Should be 2
grep "^def " backend/chatbot/mcp_tools/hadith_tools.py | wc -l  # Should be 2
```

---

## Milestone 3: Tool Registry & Binding

### Objective
Create central registry that maps tool names to implementations.

### 3.1 Implement Tool Registry

**File:** `backend/chatbot/mcp_tools/registry.py`

```python
"""
MCP Tool Registry

Central registry mapping tool names to implementations.
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
        Tool execution result as dict
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
        elif hasattr(result, 'model_dump'):
            return result.model_dump()
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

### Deliverables
- ✅ `registry.py` implemented with all 12 tools registered
- ✅ `execute_tool()` function works correctly
- ✅ `get_tool_registry()` returns initialized registry

### Validation
```python
# Test registry
from chatbot.mcp_tools.registry import get_tool_registry

registry = get_tool_registry()
print(f"Registered tools: {len(registry.list_tools())}")  # Should be 12
print(f"Has create_task: {registry.has('create_task')}")  # Should be True
print(f"All tools: {registry.list_tools()}")
```

---

## Milestone 4: Agent Configuration Update

### Objective
Update agent to use the new tool registry.

### 4.1 Update Agent Configuration

**File:** `backend/chatbot/agent/config.py`

**Add tool declarations:**
```python
"""
Agent Configuration
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

# Validate all tools are valid
from chatbot.mcp_tools.constants import ALL_TOOL_NAMES

invalid_tools = set(AGENT_TOOLS) - ALL_TOOL_NAMES
if invalid_tools:
    raise ValueError(f"Invalid tool names in AGENT_TOOLS: {invalid_tools}")
```

### 4.2 Update Agent Runtime

**File:** `backend/chatbot/agent/agent.py`

**Current code (BEFORE):**
```python
# OLD - Current implementation
from chatbot.mcp_tools import execute_tool

# In run_agent():
if intent == "create_task":
    result = execute_tool("create_task", user_id, ...)
    if result.get('error') == 'TOOL_NOT_FOUND':
        return "❌ Failed to create task: TOOL_NOT_FOUND"
```

**Updated code (AFTER):**
```python
# NEW - Updated implementation
from chatbot.mcp_tools.registry import execute_tool
from chatbot.mcp_tools.constants import TOOL_CREATE_TASK

# In run_agent():
if intent == "create_task":
    result = execute_tool(TOOL_CREATE_TASK, user_id, ...)

    # TOOL_NOT_FOUND should never happen now
    if result.get('error') == 'TOOL_NOT_FOUND':
        logger.critical(
            f"CRITICAL BUG: Tool '{TOOL_CREATE_TASK}' not found! "
            f"This should never happen."
        )
        # Still handle gracefully for user
        return "System error: Tool not available. Please contact support."

    if result.get('success'):
        task = result.get('data', {})
        return f"✅ Task created successfully!\n\nTitle: {task.get('title')}\n..."
    else:
        error_msg = result.get('error_message', 'Unknown error')
        return f"❌ Failed to create task: {error_msg}"
```

**Changes to make:**
1. Import constants instead of string literals
2. Use `execute_tool` from registry
3. Handle success/failure properly
4. Log critical error if TOOL_NOT_FOUND (but shouldn't happen)

### 4.3 Remove Old Tool Stubs

**Files to check and clean:**
- `backend/chatbot/mcp_tools.py` - If exists, delete or replace
- Any old tool stub files

### Deliverables
- ✅ Agent uses tool constants (no string literals)
- ✅ Agent calls `execute_tool` from registry
- ✅ All intent handling updated for 12 tools
- ✅ Old stubs removed

### Validation
```bash
# Verify no string literal tool names in agent
grep -n '"create_task"' backend/chatbot/agent/agent.py  # Should find none
grep -n 'TOOL_CREATE_TASK' backend/chatbot/agent/agent.py  # Should find constant usage

# Verify imports
grep -n "from chatbot.mcp_tools" backend/chatbot/agent/agent.py
```

---

## Milestone 5: Startup Validation

### Objective
Add startup check to verify all tools are registered.

### 5.1 Add Startup Validation to Main

**File:** `backend/main.py`

**Add validation function:**
```python
from chatbot.mcp_tools.registry import get_tool_registry
from chatbot.agent.config import AGENT_TOOLS
import logging

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def validate_mcp_tools():
    """
    Validate that all agent tools are registered.

    CRITICAL: This prevents the application from starting if
    any tools are missing, avoiding TOOL_NOT_FOUND errors at runtime.
    """
    logger.info("Validating MCP tool registration...")

    registry = get_tool_registry()
    registered_tools = registry.list_tools()

    missing_tools = []
    for tool_name in AGENT_TOOLS:
        if not registry.has(tool_name):
            missing_tools.append(tool_name)

    if missing_tools:
        error_msg = (
            f"CRITICAL: The following tools are declared in AGENT_TOOLS "
            f"but not registered in the tool registry: {missing_tools}. "
            f"This will cause TOOL_NOT_FOUND errors at runtime. "
            f"Application startup FAILED."
        )
        logger.critical(error_msg)
        raise RuntimeError(error_msg)

    logger.info(
        f"✅ MCP tool validation passed: "
        f"{len(AGENT_TOOLS)} tools declared, "
        f"{len(registered_tools)} tools registered"
    )
    logger.debug(f"Registered tools: {registered_tools}")
```

### Deliverables
- ✅ Startup validation added to `main.py`
- ✅ Application fails to start if tools missing
- ✅ Clear error message indicates which tools are missing

### Validation
```bash
# Start server - should pass validation
python -m uvicorn main:app --reload

# Expected log output:
# INFO:     Validating MCP tool registration...
# INFO:     ✅ MCP tool validation passed: 12 tools declared, 12 tools registered

# If tools missing, should see:
# CRITICAL: The following tools are declared but not registered: ['missing_tool']
# ERROR:    Application startup FAILED
```

---

## Milestone 6: Basic Tool Testing

### Objective
Test each tool directly to verify HTTP integration works.

### 6.1 Create Tool Test Script

**File:** `backend/test_mcp_tools.py`

```python
"""
Direct MCP Tool Testing Script

Tests each tool directly to verify:
- Tool can be called
- HTTP request succeeds
- Backend responds correctly
- Data is returned
"""

import sys
import logging
from chatbot.mcp_tools.registry import execute_tool
from chatbot.mcp_tools.constants import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_create_task():
    """Test create_task tool"""
    logger.info("Testing create_task...")

    result = execute_tool(
        TOOL_CREATE_TASK,
        user_id=1,
        title="Test Fajr Task",
        description="Read Quran after Fajr",
        priority="high",
        linked_prayer="Fajr"
    )

    assert result['success'], f"create_task failed: {result.get('error_message')}"
    assert 'data' in result, "No data returned"
    assert 'id' in result['data'], "No task ID returned"

    logger.info(f"✅ create_task passed: Task ID {result['data']['id']}")
    return result['data']['id']


def test_list_tasks():
    """Test list_tasks tool"""
    logger.info("Testing list_tasks...")

    result = execute_tool(
        TOOL_LIST_TASKS,
        user_id=1,
        status="pending"
    )

    assert result['success'], f"list_tasks failed: {result.get('error_message')}"
    assert 'data' in result, "No data returned"

    task_count = len(result['data'])
    logger.info(f"✅ list_tasks passed: Found {task_count} tasks")


def test_search_masjids():
    """Test search_masjids tool"""
    logger.info("Testing search_masjids...")

    result = execute_tool(
        TOOL_SEARCH_MASJIDS,
        user_id=1,
        area="North Nazimabad"
    )

    assert result['success'], f"search_masjids failed: {result.get('error_message')}"

    logger.info("✅ search_masjids passed")


def test_get_daily_hadith():
    """Test get_daily_hadith tool"""
    logger.info("Testing get_daily_hadith...")

    result = execute_tool(
        TOOL_GET_DAILY_HADITH,
        user_id=1
    )

    assert result['success'], f"get_daily_hadith failed: {result.get('error_message')}"

    logger.info("✅ get_daily_hadith passed")


def main():
    """Run all tool tests"""
    print("=" * 60)
    print("MCP Tool Direct Testing")
    print("=" * 60)
    print()

    tests = [
        ("create_task", test_create_task),
        ("list_tasks", test_list_tasks),
        ("search_masjids", test_search_masjids),
        ("get_daily_hadith", test_get_daily_hadith),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            logger.error(f"❌ {name} FAILED: {e}")
            failed += 1
        except Exception as e:
            logger.error(f"❌ {name} ERROR: {e}", exc_info=True)
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
```

### 6.2 Create Unit Tests

**File:** `backend/chatbot/mcp_tools/__tests__/test_tasks_tools.py`

```python
import pytest
from chatbot.mcp_tools.tasks_tools import create_task, list_tasks
from chatbot.mcp_tools.base import ToolResult


def test_create_task_success():
    """Test successful task creation"""
    result = create_task(
        user_id=1,
        title="Test Task",
        description="Test description",
        priority="medium"
    )

    assert isinstance(result, ToolResult)
    assert result.success == True
    assert result.data is not None
    assert 'id' in result.data


def test_create_task_auth_required():
    """Test task creation without user_id fails"""
    result = create_task(
        user_id=None,  # Invalid
        title="Test Task"
    )

    assert result.success == False
    assert result.error == "AUTH_REQUIRED"


def test_list_tasks():
    """Test task listing"""
    result = list_tasks(user_id=1, status="pending")

    assert isinstance(result, ToolResult)
    assert result.success == True or result.error in ["AUTH_REQUIRED", "NOT_FOUND"]
```

### Deliverables
- ✅ `test_mcp_tools.py` - Direct tool testing script
- ✅ Unit tests for each tool category
- ✅ All tests pass

### Validation
```bash
# Run direct tool tests
cd backend
python test_mcp_tools.py

# Expected output:
# Testing create_task...
# ✅ create_task passed: Task ID 123
# Testing list_tasks...
# ✅ list_tasks passed: Found 5 tasks
# ...
# Results: 4 passed, 0 failed

# Run unit tests
pytest chatbot/mcp_tools/__tests__/ -v

# Expected output:
# test_tasks_tools.py::test_create_task_success PASSED
# test_tasks_tools.py::test_list_tasks PASSED
# ...
# ===== 12 passed in 2.3s =====
```

---

## Milestone 7: Chatbot Flow Smoke Tests

### Objective
Test complete conversation flows to ensure no TOOL_NOT_FOUND errors.

### 7.1 Create Conversation Test Script

**File:** `backend/test_chatbot_flows.py`

```python
"""
Chatbot Conversation Flow Tests

Tests complete conversation flows through the chat API.
"""

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000/api/v1/chat/"


def chat(message: str, user_id: int = None):
    """Send a chat message"""
    payload = {
        "message": message,
        "user_id": user_id,
        "conversation_history": []
    }

    response = requests.post(API_URL, json=payload)
    response.raise_for_status()
    return response.json()


def test_create_task_flow():
    """Test: User creates a task via chat"""
    logger.info("Testing task creation flow...")

    response = chat("Fajr ka task bana do", user_id=1)

    assert response['success'], f"Chat failed: {response.get('error_message')}"
    assert 'TOOL_NOT_FOUND' not in response['message'], \
        "TOOL_NOT_FOUND error occurred!"
    assert 'task' in response['message'].lower(), \
        "Response doesn't mention task"

    logger.info(f"✅ Create task flow passed: {response['message'][:100]}")


def test_list_tasks_flow():
    """Test: User lists tasks via chat"""
    logger.info("Testing list tasks flow...")

    response = chat("Mujhe mere tasks dikhao", user_id=1)

    assert response['success'], f"Chat failed: {response.get('error_message')}"
    assert 'TOOL_NOT_FOUND' not in response['message'], \
        "TOOL_NOT_FOUND error occurred!"

    logger.info(f"✅ List tasks flow passed")


def test_search_masjids_flow():
    """Test: User searches for masjids"""
    logger.info("Testing masjid search flow...")

    response = chat("North Nazimabad mein konsi masjid hai?", user_id=None)

    assert response['success'], f"Chat failed: {response.get('error_message')}"
    assert 'TOOL_NOT_FOUND' not in response['message'], \
        "TOOL_NOT_FOUND error occurred!"
    assert 'masjid' in response['message'].lower(), \
        "Response doesn't mention masjid"

    logger.info(f"✅ Masjid search flow passed")


def test_get_hadith_flow():
    """Test: User requests daily hadith"""
    logger.info("Testing hadith flow...")

    response = chat("Aaj ki hadith sunao", user_id=1)

    assert response['success'], f"Chat failed: {response.get('error_message')}"
    assert 'TOOL_NOT_FOUND' not in response['message'], \
        "TOOL_NOT_FOUND error occurred!"

    logger.info(f"✅ Hadith flow passed")


def test_auth_required_flow():
    """Test: User tries to create task without login"""
    logger.info("Testing auth required flow...")

    response = chat("Create a task", user_id=None)

    # Should get auth required, not TOOL_NOT_FOUND
    assert response['success'] == False, "Should fail without auth"
    assert response['error'] == 'authentication_required', \
        f"Wrong error: {response.get('error')}"
    assert 'TOOL_NOT_FOUND' not in str(response), \
        "TOOL_NOT_FOUND should not appear"

    logger.info(f"✅ Auth required flow passed")


def main():
    """Run all conversation flow tests"""
    print("=" * 60)
    print("Chatbot Conversation Flow Tests")
    print("=" * 60)
    print()

    tests = [
        ("Create Task", test_create_task_flow),
        ("List Tasks", test_list_tasks_flow),
        ("Search Masjids", test_search_masjids_flow),
        ("Get Hadith", test_get_hadith_flow),
        ("Auth Required", test_auth_required_flow),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            logger.error(f"❌ {name} FAILED: {e}")
            failed += 1
        except Exception as e:
            logger.error(f"❌ {name} ERROR: {e}", exc_info=True)
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        print()
        print("❌ CRITICAL: Conversation flows have errors!")
        print("   TOOL_NOT_FOUND or other issues detected.")
        print("   Phase III is NOT complete until all tests pass.")
        return 1
    else:
        print()
        print("✅ SUCCESS: All conversation flows working!")
        print("   No TOOL_NOT_FOUND errors detected.")
        return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### 7.2 Manual UI Testing Checklist

**Create test checklist:** `backend/CHATBOT_MANUAL_TEST_CHECKLIST.md`

```markdown
# Chatbot Manual Testing Checklist

Test each conversation flow manually through the chat UI.

## Prerequisites
- [ ] Backend running: `./start_chatbot.sh`
- [ ] Frontend running: `cd ../frontend && npm run dev`
- [ ] User logged in (user_id available)

## Test Cases

### Task Management
- [ ] Create Task: "Fajr ka task bana do"
  - Expected: Task created, no TOOL_NOT_FOUND
  - Verify: Check `/api/v1/tasks` - task exists in DB

- [ ] List Tasks: "Mere tasks dikhao"
  - Expected: Task list displayed, no TOOL_NOT_FOUND

- [ ] Complete Task: "Task 1 complete karo"
  - Expected: Task marked completed
  - Verify: Check DB - task.completed = true

### Masjid Search
- [ ] Search Masjids: "North Nazimabad mein masjid"
  - Expected: Masjid list displayed, no TOOL_NOT_FOUND

- [ ] Get Prayer Times: "Namaz ka time kya hai"
  - Expected: Prayer times shown, no TOOL_NOT_FOUND

### Hadith
- [ ] Daily Hadith: "Aaj ki hadith sunao"
  - Expected: Hadith displayed, no TOOL_NOT_FOUND

### Auth Checks
- [ ] Create Task (No Login): "Create a task" (user_id=null)
  - Expected: "Please log in" message
  - NOT Expected: TOOL_NOT_FOUND

## Success Criteria
- [ ] All test cases pass
- [ ] ZERO TOOL_NOT_FOUND errors
- [ ] All features work end-to-end
```

### Deliverables
- ✅ `test_chatbot_flows.py` - Automated conversation tests
- ✅ `CHATBOT_MANUAL_TEST_CHECKLIST.md` - Manual testing guide
- ✅ All automated tests pass
- ✅ All manual tests pass

### Validation
```bash
# Run automated conversation tests
cd backend
python test_chatbot_flows.py

# Expected output:
# Testing task creation flow...
# ✅ Create task flow passed
# Testing list tasks flow...
# ✅ List tasks flow passed
# ...
# Results: 5 passed, 0 failed
# ✅ SUCCESS: All conversation flows working!
```

---

## Milestone 8: Documentation Updates

### Objective
Update all documentation to reflect completed MCP tool implementation.

### 8.1 Update Phase III Specification

**File:** `docs/phase3_spec.md`

**Sections to update:**

1. **Tool Reference Table:**
```markdown
## MCP Tools - Implementation Status

| Tool Name | Status | Backend Endpoint | Auth Required |
|-----------|--------|------------------|---------------|
| create_task | ✅ Implemented | POST /api/v1/tasks | Yes |
| list_tasks | ✅ Implemented | GET /api/v1/tasks | Yes |
| update_task | ✅ Implemented | PUT /api/v1/tasks/{id} | Yes |
| delete_task | ✅ Implemented | DELETE /api/v1/tasks/{id} | Yes |
| complete_task | ✅ Implemented | PATCH /api/v1/tasks/{id}/complete | Yes |
| list_masjids | ✅ Implemented | GET /api/v1/masjids | No |
| get_masjid_details | ✅ Implemented | GET /api/v1/masjids/{id} | No |
| search_masjids | ✅ Implemented | GET /api/v1/masjids/search | No |
| get_prayer_times | ✅ Implemented | GET /api/v1/masjids/{id} | No |
| get_current_prayer | ✅ Implemented | GET /api/v1/masjids/{id}/current-prayer | No |
| get_daily_hadith | ✅ Implemented | GET /api/v1/hadith/daily | No |
| get_random_hadith | ✅ Implemented | GET /api/v1/hadith/random | No |

**Status:** All 12 tools fully implemented ✅
**TOOL_NOT_FOUND Errors:** ELIMINATED ✅
```

2. **Implementation Status:**
```markdown
## Phase III Status: COMPLETE ✅

- ✅ All MCP tools implemented and registered
- ✅ Tool registry system in place
- ✅ Startup validation prevents missing tools
- ✅ All conversation flows tested
- ✅ No TOOL_NOT_FOUND errors
```

### 8.2 Create MCP Tools Developer Guide

**File:** `docs/phase3_mcp_tools.md`

**Content:**
```markdown
# Phase III: MCP Tools Developer Guide

## Overview

All 12 MCP tools are fully implemented and integrated with the chatbot agent.

## Architecture

### File Structure
\`\`\`
backend/chatbot/mcp_tools/
├── constants.py         # Tool name constants
├── registry.py          # Central registry
├── base.py              # ToolResult, BackendClient
├── tasks_tools.py       # 5 task tools
├── masjid_tools.py      # 3 masjid tools
├── prayer_tools.py      # 2 prayer tools
├── hadith_tools.py      # 2 hadith tools
└── __tests__/           # Unit tests
\`\`\`

### Tool Flow
\`\`\`
User Message → Agent → execute_tool() → Registry → Tool Function → HTTP Request → Backend → Response
\`\`\`

## Adding a New Tool

1. **Add constant** to `constants.py`:
   \`\`\`python
   TOOL_NEW_FEATURE = "new_feature"
   \`\`\`

2. **Implement function** in appropriate file:
   \`\`\`python
   def new_feature(user_id: int, **kwargs) -> ToolResult:
       # Implementation
       pass
   \`\`\`

3. **Register** in `registry.py`:
   \`\`\`python
   self.register(TOOL_NEW_FEATURE, new_feature)
   \`\`\`

4. **Add to agent** in `agent/config.py`:
   \`\`\`python
   AGENT_TOOLS = [
       # ...
       TOOL_NEW_FEATURE,
   ]
   \`\`\`

5. **Restart** - validation will verify registration

## Testing

\`\`\`bash
# Direct tool test
python test_mcp_tools.py

# Conversation flow test
python test_chatbot_flows.py

# Unit tests
pytest chatbot/mcp_tools/__tests__/
\`\`\`

## Troubleshooting

### TOOL_NOT_FOUND Error

This error means a tool is used but not registered.

**Steps to fix:**
1. Check `constants.py` - is the tool name defined?
2. Check `registry.py` - is the tool registered?
3. Check implementation file - does the function exist?
4. Check `agent/config.py` - is it in AGENT_TOOLS?
5. Restart server - startup validation will catch it

**This should NEVER happen in production!**
```

### 8.3 Update Main README

**File:** `README.md`

**Update Phase III section:**
```markdown
## Phase III: AI-Powered Chatbot ✅ COMPLETE

The SalaatFlow chatbot is **fully functional** with **complete MCP tool integration**.

### Features
- ✅ Create, list, update, delete spiritual tasks via natural language
- ✅ Find masjids and get prayer times through conversation
- ✅ Get daily hadith via chat
- ✅ Bilingual support (English & Urdu)
- ✅ Context-aware conversations with history
- ✅ Robust error handling with specific error types
- ✅ **All 12 MCP tools implemented and tested**

### MCP Tools Status
**All chatbot tools are implemented and registered.**

✅ **No TOOL_NOT_FOUND errors occur in a correctly configured system.**

The system validates tool availability on startup and will **fail to start** if any tools are missing.

### Quick Test
\`\`\`bash
# Start backend
cd backend
./start_chatbot.sh

# Run conversation tests
python test_chatbot_flows.py
\`\`\`

### Documentation
- [Phase III Specification](docs/PHASE3_MCP_TOOLS_SPECIFICATION.md)
- [MCP Tools Developer Guide](docs/phase3_mcp_tools.md)
- [API Testing Examples](backend/API_TESTING_EXAMPLES.md)
```

### Deliverables
- ✅ `docs/phase3_spec.md` updated with implementation status
- ✅ `docs/phase3_mcp_tools.md` created with developer guide
- ✅ `README.md` updated with Phase III completion status

### Validation
```bash
# Check documentation exists
ls -la docs/phase3*.md
ls -la docs/PHASE3*.md

# Verify README mentions "COMPLETE"
grep "COMPLETE" README.md
```

---

## Implementation Checklist Summary

### Phase 1: Discovery (Milestone 1)
- [ ] Inspect agent code for current tool usage
- [ ] Create `CURRENT_TOOL_INVENTORY.md`
- [ ] Create `TOOL_NAME_ALIGNMENT.md`
- [ ] Confirm 12 tools to implement

### Phase 2: Foundation (Milestones 2-3)
- [ ] Create `mcp_tools/` directory structure
- [ ] Implement `constants.py` with all 12 tool names
- [ ] Implement `base.py` with ToolResult and BackendClient
- [ ] Implement `exceptions.py`
- [ ] Implement all 5 task tools in `tasks_tools.py`
- [ ] Implement all 3 masjid tools in `masjid_tools.py`
- [ ] Implement all 2 prayer tools in `prayer_tools.py`
- [ ] Implement all 2 hadith tools in `hadith_tools.py`
- [ ] Implement `registry.py` with all tools registered

### Phase 3: Integration (Milestone 4-5)
- [ ] Update `agent/config.py` with AGENT_TOOLS list
- [ ] Update `agent/agent.py` to use constants and execute_tool
- [ ] Add startup validation to `main.py`
- [ ] Remove old tool stubs

### Phase 4: Testing (Milestones 6-7)
- [ ] Create `test_mcp_tools.py` direct testing script
- [ ] Create unit tests for all tools
- [ ] Create `test_chatbot_flows.py` conversation tests
- [ ] Create `CHATBOT_MANUAL_TEST_CHECKLIST.md`
- [ ] Run all tests - ALL MUST PASS

### Phase 5: Documentation (Milestone 8)
- [ ] Update `docs/phase3_spec.md`
- [ ] Create `docs/phase3_mcp_tools.md`
- [ ] Update `README.md`

---

## Success Criteria

Phase III MCP Tools implementation is **COMPLETE** when:

1. ✅ All 12 tools implemented in `mcp_tools/` modules
2. ✅ All 12 tools registered in `registry.py`
3. ✅ All 12 tools declared in `agent/config.py`
4. ✅ Startup validation passes (server starts successfully)
5. ✅ Direct tool tests pass (`test_mcp_tools.py`)
6. ✅ Unit tests pass (pytest)
7. ✅ Conversation flow tests pass (`test_chatbot_flows.py`)
8. ✅ Manual UI tests pass (checklist)
9. ✅ **ZERO `TOOL_NOT_FOUND` errors in ANY scenario**
10. ✅ All documentation updated

---

## Critical Failure Conditions

The following are **BLOCKING FAILURES** that prevent Phase III completion:

❌ **ANY `TOOL_NOT_FOUND` error in any test**
❌ **ANY tool not registered in registry**
❌ **Startup validation fails**
❌ **Any conversation flow test fails**
❌ **Backend HTTP integration not working**
❌ **Tests not passing**

---

## Timeline Estimate

| Milestone | Tasks | Estimated Time |
|-----------|-------|----------------|
| 1. Discovery | Inspect, document | 1-2 hours |
| 2. Foundation (Tools) | Implement 12 tools | 4-6 hours |
| 3. Registry | Registry & binding | 1-2 hours |
| 4. Integration | Agent updates | 2-3 hours |
| 5. Startup | Validation | 1 hour |
| 6. Tool Tests | Direct & unit tests | 2-3 hours |
| 7. Flow Tests | Conversation tests | 2-3 hours |
| 8. Documentation | Docs update | 2-3 hours |

**Total:** 15-23 hours (2-3 working days)

---

## Next Steps

1. **Read** this plan thoroughly
2. **Start with Milestone 1** - Discovery
3. **Proceed sequentially** through milestones
4. **Test continuously** - don't wait until the end
5. **Document as you go** - update status in real-time
6. **Validate at each milestone** - don't skip validation steps
7. **Fix issues immediately** - don't accumulate technical debt

---

**END OF IMPLEMENTATION PLAN**

**Version:** 1.0
**Date:** 2025-12-30
**Status:** Ready for Execution
**Critical Goal:** **ELIMINATE ALL TOOL_NOT_FOUND ERRORS**
