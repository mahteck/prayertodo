"""
MCP Tools - Tool Name Constants
Centralized tool name definitions to ensure consistency across the codebase

CRITICAL: All tool names MUST be referenced from this file.
NO string literals for tool names elsewhere in the code.
"""

# ============================================================================
# TASK MANAGEMENT TOOLS (5 tools)
# ============================================================================

TOOL_CREATE_TASK = "create_task"
TOOL_LIST_TASKS = "list_tasks"
TOOL_UPDATE_TASK = "update_task"
TOOL_DELETE_TASK = "delete_task"
TOOL_COMPLETE_TASK = "complete_task"

# ============================================================================
# MASJID TOOLS (3 tools)
# ============================================================================

TOOL_LIST_MASJIDS = "list_masjids"
TOOL_GET_MASJID_DETAILS = "get_masjid_details"
TOOL_SEARCH_MASJIDS = "search_masjids"

# ============================================================================
# PRAYER TIMES TOOLS (2 tools)
# ============================================================================

TOOL_GET_PRAYER_TIMES = "get_prayer_times"
TOOL_GET_CURRENT_PRAYER = "get_current_prayer"

# ============================================================================
# HADITH TOOLS (2 tools)
# ============================================================================

TOOL_GET_DAILY_HADITH = "get_daily_hadith"
TOOL_GET_RANDOM_HADITH = "get_random_hadith"

# ============================================================================
# TOOL REGISTRY
# ============================================================================

# All task management tools
TASK_MANAGEMENT_TOOLS = [
    TOOL_CREATE_TASK,
    TOOL_LIST_TASKS,
    TOOL_UPDATE_TASK,
    TOOL_DELETE_TASK,
    TOOL_COMPLETE_TASK,
]

# All masjid tools
MASJID_TOOLS = [
    TOOL_LIST_MASJIDS,
    TOOL_GET_MASJID_DETAILS,
    TOOL_SEARCH_MASJIDS,
]

# All prayer time tools
PRAYER_TOOLS = [
    TOOL_GET_PRAYER_TIMES,
    TOOL_GET_CURRENT_PRAYER,
]

# All hadith tools
HADITH_TOOLS = [
    TOOL_GET_DAILY_HADITH,
    TOOL_GET_RANDOM_HADITH,
]

# Complete list of all 12 required tools
ALL_TOOL_NAMES = (
    TASK_MANAGEMENT_TOOLS +
    MASJID_TOOLS +
    PRAYER_TOOLS +
    HADITH_TOOLS
)

# Validation
assert len(ALL_TOOL_NAMES) == 12, f"Expected 12 tools, got {len(ALL_TOOL_NAMES)}"
assert len(set(ALL_TOOL_NAMES)) == 12, "Tool names must be unique"

# ============================================================================
# TOOL CATEGORIES (for logging and organization)
# ============================================================================

TOOL_CATEGORIES = {
    "task_management": TASK_MANAGEMENT_TOOLS,
    "masjid": MASJID_TOOLS,
    "prayer": PRAYER_TOOLS,
    "hadith": HADITH_TOOLS,
}


def get_tool_category(tool_name: str) -> str:
    """
    Get the category of a tool by its name

    Args:
        tool_name: Tool name to look up

    Returns:
        Category name or "unknown"
    """
    for category, tools in TOOL_CATEGORIES.items():
        if tool_name in tools:
            return category
    return "unknown"


def validate_tool_name(tool_name: str) -> bool:
    """
    Validate that a tool name is in the registry

    Args:
        tool_name: Tool name to validate

    Returns:
        True if tool name is valid, False otherwise
    """
    return tool_name in ALL_TOOL_NAMES
