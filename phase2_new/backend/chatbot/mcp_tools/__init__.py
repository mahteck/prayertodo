"""
MCP Tools Package
Centralized export of all MCP tools and registry

This package provides all MCP tools for the SalaatFlow AI agent.
"""

from chatbot.mcp_tools.registry import (
    ToolRegistry,
    get_tool_registry,
    execute_tool,
    validate_all_tools,
)

from chatbot.mcp_tools.constants import (
    ALL_TOOL_NAMES,
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
)

__all__ = [
    # Registry functions
    "ToolRegistry",
    "get_tool_registry",
    "execute_tool",
    "validate_all_tools",
    # Tool name constants
    "ALL_TOOL_NAMES",
    "TOOL_CREATE_TASK",
    "TOOL_LIST_TASKS",
    "TOOL_UPDATE_TASK",
    "TOOL_DELETE_TASK",
    "TOOL_COMPLETE_TASK",
    "TOOL_LIST_MASJIDS",
    "TOOL_GET_MASJID_DETAILS",
    "TOOL_SEARCH_MASJIDS",
    "TOOL_GET_PRAYER_TIMES",
    "TOOL_GET_CURRENT_PRAYER",
    "TOOL_GET_DAILY_HADITH",
    "TOOL_GET_RANDOM_HADITH",
]
