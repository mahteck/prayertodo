# Phase III MCP Tools Specification - Executive Summary

## Document Overview

**Primary Document:** `PHASE3_MCP_TOOLS_SPECIFICATION.md`
**Purpose:** Eliminate `TOOL_NOT_FOUND` errors by requiring full implementation of all MCP tools
**Status:** Ready for AI-driven implementation
**Version:** 2.0 (Refined)

## Critical Changes from Previous Specification

### ❌ DEPRECATED Behavior (No Longer Acceptable)

The following are **NO LONGER VALID** statements:

> "The `TOOL_NOT_FOUND` error means the MCP tools are not implemented yet. This is expected."

> "The chatbot is working correctly, but the task management tools need to be set up."

> "MCP tools return TOOL_NOT_FOUND (expected - not implemented yet)"

### ✅ NEW Requirements (Mandatory)

1. **All 12 MCP tools MUST be fully implemented and registered**
2. **`TOOL_NOT_FOUND` is now classified as a BUG, not an expected state**
3. **Startup validation MUST verify all tools exist before server starts**
4. **Any tool not registered MUST cause startup failure**
5. **All conversation flows MUST work end-to-end without errors**

## Tool Registry (12 Required Tools)

### Task Management (5 tools)
1. `create_task` - Create spiritual task → `POST /api/v1/tasks`
2. `list_tasks` - List user tasks → `GET /api/v1/tasks`
3. `update_task` - Update task → `PUT /api/v1/tasks/{id}`
4. `delete_task` - Delete task → `DELETE /api/v1/tasks/{id}`
5. `complete_task` - Mark completed → `PATCH /api/v1/tasks/{id}/complete`

### Masjid Tools (3 tools)
6. `list_masjids` - List masjids → `GET /api/v1/masjids`
7. `get_masjid_details` - Get details → `GET /api/v1/masjids/{id}`
8. `search_masjids` - Search masjids → `GET /api/v1/masjids/search`

### Prayer Times (2 tools)
9. `get_prayer_times` - Get prayer schedule → `GET /api/v1/masjids/{id}`
10. `get_current_prayer` - Current/next prayer → `GET /api/v1/masjids/{id}/current-prayer`

### Hadith (2 tools)
11. `get_daily_hadith` - Daily hadith → `GET /api/v1/hadith/daily`
12. `get_random_hadith` - Random hadith → `GET /api/v1/hadith/random`

## Architecture Requirements

### File Structure (MUST BE CREATED)

```
backend/chatbot/mcp_tools/
├── __init__.py                  # Package exports
├── constants.py                 # ⭐ All tool name constants (REQUIRED)
├── registry.py                  # ⭐ Central tool registry (REQUIRED)
├── base.py                      # Base classes, ToolResult, BackendClient
├── exceptions.py                # Custom exceptions
├── tasks_tools.py               # 5 task management tools
├── masjid_tools.py              # 3 masjid tools
├── prayer_tools.py              # 2 prayer time tools
├── hadith_tools.py              # 2 hadith tools
└── __tests__/                   # Unit tests for all tools
    ├── test_tasks_tools.py
    ├── test_masjid_tools.py
    ├── test_prayer_tools.py
    └── test_hadith_tools.py
```

### Tool Name Consistency (CRITICAL)

**MANDATORY RULE:**
- ALL tool names MUST be defined as constants in `constants.py`
- NO string literals for tool names anywhere else
- Constants MUST be used in:
  - Agent configuration
  - Tool implementations
  - Registry registration
  - Tests

**Example:**
```python
# constants.py
TOOL_CREATE_TASK = "create_task"

# tasks_tools.py
from .constants import TOOL_CREATE_TASK

def create_task(...):  # Function name matches constant
    ...

# registry.py
from .constants import TOOL_CREATE_TASK
from .tasks_tools import create_task

registry.register(TOOL_CREATE_TASK, create_task)  # Uses constant

# agent/config.py
from chatbot.mcp_tools.constants import TOOL_CREATE_TASK

AGENT_TOOLS = [TOOL_CREATE_TASK, ...]  # Uses constant
```

## Standard Tool Interface

### Input Format (ALL TOOLS)

```python
def tool_name(
    user_id: int,              # REQUIRED - Always first parameter
    **kwargs                   # Tool-specific parameters
) -> ToolResult:
```

### Output Format (ALL TOOLS)

```python
class ToolResult(BaseModel):
    success: bool              # True = success, False = error
    data: Optional[Dict]       # Result data if success
    error: Optional[str]       # Error code if failure
    error_message: Optional[str]  # User-friendly message if failure
```

### Error Handling (MANDATORY)

Each tool MUST handle:
1. **Network errors** → `ToolResult(success=False, error="NETWORK_ERROR")`
2. **HTTP 401** → `ToolResult(success=False, error="AUTH_REQUIRED")`
3. **HTTP 404** → `ToolResult(success=False, error="NOT_FOUND")`
4. **HTTP 5xx** → `ToolResult(success=False, error="SERVER_ERROR")`
5. **Validation errors** → `ToolResult(success=False, error="VALIDATION_ERROR")`

**FORBIDDEN:**
- ❌ Silent failures
- ❌ Swallowing exceptions
- ❌ Generic error messages
- ❌ Returning success=true when operation failed

## Integration Requirements

### 1. Agent Configuration Update

**File:** `backend/chatbot/agent/config.py`

```python
from chatbot.mcp_tools.constants import *

AGENT_TOOLS = [
    TOOL_CREATE_TASK,
    TOOL_LIST_TASKS,
    # ... all 12 tools ...
]

# Validation
assert set(AGENT_TOOLS).issubset(ALL_TOOL_NAMES)
```

### 2. Agent Runtime Update

**File:** `backend/chatbot/agent/agent.py`

```python
from chatbot.mcp_tools.registry import execute_tool

# OLD (DEPRECATED):
try:
    result = execute_tool("create_task", user_id, ...)
except Exception:
    return "TOOL_NOT_FOUND"  # ❌ NO LONGER ACCEPTABLE

# NEW (REQUIRED):
result = execute_tool("create_task", user_id, ...)
# If TOOL_NOT_FOUND, it's a BUG that should never happen
```

### 3. Startup Validation (REQUIRED)

**File:** `backend/main.py`

```python
@app.on_event("startup")
async def validate_mcp_tools():
    """CRITICAL: Validate all tools exist on startup"""
    registry = get_tool_registry()

    missing = [t for t in AGENT_TOOLS if not registry.has(t)]

    if missing:
        raise RuntimeError(
            f"CRITICAL: Tools not registered: {missing}. "
            f"Application cannot start."
        )

    logger.info(f"✅ All {len(AGENT_TOOLS)} tools registered")
```

## Acceptance Criteria (ALL MUST PASS)

### 1. Tool Registration Test
```python
✅ All 12 tools are registered in registry
✅ All 12 tools are declared in AGENT_TOOLS
✅ Startup validation passes
✅ No missing tools
```

### 2. Conversation Flow Tests

Each flow MUST work end-to-end:

```python
✅ "Fajr ka task bana do" → Task created in DB
✅ "Mere tasks dikhao" → Tasks retrieved and displayed
✅ "Task 1 complete karo" → Task marked completed
✅ "North Nazimabad mein masjid" → Masjids listed
✅ "Namaz ka time kya hai" → Prayer times shown
✅ "Aaj ki hadith sunao" → Hadith displayed
```

### 3. NO TOOL_NOT_FOUND (CRITICAL)

```python
❌ FAILS if ANY conversation returns TOOL_NOT_FOUND
✅ PASSES only if ALL tools execute successfully
```

### 4. Error Handling Test

```python
✅ Invalid parameters → VALIDATION_ERROR
✅ Not authenticated → AUTH_REQUIRED
✅ Backend down → NETWORK_ERROR
✅ Resource not found → NOT_FOUND
```

## Implementation Checklist

### Phase 1: Foundation (CRITICAL)
- [ ] Create `mcp_tools/` directory structure
- [ ] Implement `constants.py` with ALL 12 tool names
- [ ] Implement `base.py` with ToolResult and BackendClient
- [ ] Implement `exceptions.py`
- [ ] Implement `registry.py` with ToolRegistry class

### Phase 2: Tool Implementation
- [ ] Implement all 5 task tools in `tasks_tools.py`
- [ ] Implement all 3 masjid tools in `masjid_tools.py`
- [ ] Implement all 2 prayer tools in `prayer_tools.py`
- [ ] Implement all 2 hadith tools in `hadith_tools.py`
- [ ] Register ALL tools in registry.py

### Phase 3: Integration
- [ ] Update `agent/config.py` with AGENT_TOOLS
- [ ] Update `agent/agent.py` to use execute_tool
- [ ] Add startup validation to `main.py`
- [ ] Remove all "TOOL_NOT_FOUND expected" handling

### Phase 4: Testing
- [ ] Write unit tests for each tool
- [ ] Write integration tests for each flow
- [ ] Verify NO TOOL_NOT_FOUND in any scenario
- [ ] Test all error conditions

### Phase 5: Documentation
- [ ] Update `docs/phase3_spec.md`
- [ ] Create `docs/phase3_mcp_tools.md`
- [ ] Update `README.md`
- [ ] Add inline documentation

## Success Metrics

Phase III is **COMPLETE** when:

1. ✅ All 12 tools implemented and tested
2. ✅ Startup validation passes
3. ✅ All acceptance tests pass
4. ✅ ZERO `TOOL_NOT_FOUND` errors in any scenario
5. ✅ All conversation flows work end-to-end
6. ✅ Error handling is robust
7. ✅ Documentation is complete
8. ✅ Code follows specification exactly

## Quick Reference

### Tool Call Flow

```
1. User sends message: "Fajr ka task bana do"
   ↓
2. Agent detects intent: create_task
   ↓
3. Agent calls: execute_tool("create_task", user_id=1, title="Fajr", ...)
   ↓
4. Registry finds tool: create_task function
   ↓
5. Tool makes HTTP request: POST /api/v1/tasks
   ↓
6. Backend creates task in DB
   ↓
7. Tool returns: ToolResult(success=True, data={task})
   ↓
8. Agent formats response: "✅ Task created successfully!"
   ↓
9. User sees message
```

### Error Classification

| Error Code | Meaning | User Action |
|------------|---------|-------------|
| `TOOL_NOT_FOUND` | **BUG** - Tool not registered | Fix immediately - fails acceptance |
| `AUTH_REQUIRED` | Expected - User needs to log in | Prompt user to sign in |
| `VALIDATION_ERROR` | Expected - Invalid input | Show validation message |
| `NOT_FOUND` | Expected - Resource doesn't exist | Inform user |
| `SERVER_ERROR` | Expected - Backend issue | Show error, retry later |
| `NETWORK_ERROR` | Expected - Connection issue | Check connectivity |

## Key Differences from Previous Spec

| Aspect | Old Spec | New Spec |
|--------|----------|----------|
| TOOL_NOT_FOUND | "Expected, tools not implemented" | "BUG - MUST be fixed" |
| Startup behavior | Can start without tools | MUST fail if tools missing |
| Testing | Optional | Mandatory for acceptance |
| Tool registration | Implicit | Explicit with validation |
| Error handling | Basic | Comprehensive and tested |
| Documentation | Minimal | Complete with examples |

## Next Steps for Implementation

1. **Read the full specification:** `PHASE3_MCP_TOOLS_SPECIFICATION.md`
2. **Follow the implementation checklist** section by section
3. **Use AI code generation** for all implementation
4. **Test continuously** - run tests after each phase
5. **Validate on startup** - ensure tools load correctly
6. **Document as you go** - update docs with actual implementation details

## References

- **Full Specification:** `docs/PHASE3_MCP_TOOLS_SPECIFICATION.md` (this document)
- **Current Status:** `backend/CHATBOT_STATUS_SUMMARY.md`
- **API Testing Guide:** `backend/API_TESTING_EXAMPLES.md`
- **Testing Guide:** `backend/CHATBOT_TESTING_GUIDE.md`

---

**CRITICAL TAKEAWAY:**

> **`TOOL_NOT_FOUND` is no longer acceptable.
> All 12 tools MUST be implemented.
> Phase III is NOT complete until all tests pass.**

---

**Version:** 2.0
**Date:** 2025-12-30
**Status:** Ready for Implementation
**Implementation Method:** AI Code Generation
