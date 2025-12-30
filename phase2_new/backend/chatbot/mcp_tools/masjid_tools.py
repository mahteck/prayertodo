"""
Masjid MCP Tools
Simplified tool names to match agent expectations and Phase III specification

These tools use direct database access to avoid circular HTTP dependencies.
"""

from chatbot.mcp_tools.base import CallableTool
from chatbot.mcp_tools.db_client import DatabaseClient
from chatbot.mcp_tools.constants import (
    TOOL_LIST_MASJIDS,
    TOOL_GET_MASJID_DETAILS,
    TOOL_SEARCH_MASJIDS,
)


# Tool 1: list_masjids
list_masjids = CallableTool(
    name=TOOL_LIST_MASJIDS,
    description="Lists all masjids, optionally filtered by area. Use this when user asks about masjids in a general area.",
    input_schema={
        "type": "object",
        "properties": {
            "area": {
                "type": "string",
                "description": "Optional area name to filter results (e.g., 'North Nazimabad', 'Gulshan', 'Clifton')"
            },
            "city": {
                "type": "string",
                "description": "Optional city name to filter results (e.g., 'Karachi')"
            }
        },
        "required": []
    },
    callable_func=DatabaseClient.list_masjids
)


# Tool 2: get_masjid_details
get_masjid_details = CallableTool(
    name=TOOL_GET_MASJID_DETAILS,
    description="Gets full details including all prayer times for a specific masjid. Use this when you have the masjid ID.",
    input_schema={
        "type": "object",
        "properties": {
            "masjid_id": {
                "type": "integer",
                "description": "ID of the masjid"
            }
        },
        "required": ["masjid_id"]
    },
    callable_func=DatabaseClient.get_masjid_details
)


# Tool 3: search_masjids
search_masjids = CallableTool(
    name=TOOL_SEARCH_MASJIDS,
    description="Searches for masjids by name or area. Use this to find specific masjids when user mentions a name or location.",
    input_schema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Optional masjid name or partial name to search for"
            },
            "area": {
                "type": "string",
                "description": "Optional area name to filter results"
            },
            "city": {
                "type": "string",
                "description": "Optional city name to filter results"
            }
        },
        "required": []
    },
    callable_func=DatabaseClient.search_masjids
)


# Export all masjid tools
ALL_MASJID_TOOLS = [
    list_masjids,
    get_masjid_details,
    search_masjids,
]
