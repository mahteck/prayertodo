"""
Prayer Times MCP Tools
Tools for retrieving prayer times and current prayer information

These tools use direct database access to avoid circular HTTP dependencies.
"""

from chatbot.mcp_tools.base import CallableTool
from chatbot.mcp_tools.db_client import DatabaseClient
from chatbot.mcp_tools.constants import (
    TOOL_GET_PRAYER_TIMES,
    TOOL_GET_CURRENT_PRAYER,
)


# Tool 1: get_prayer_times
get_prayer_times = CallableTool(
    name=TOOL_GET_PRAYER_TIMES,
    description="Gets all prayer times for a specific masjid. Returns Fajr, Dhuhr, Asr, Maghrib, Isha, and Jummah times. Use this when user asks for prayer schedule.",
    input_schema={
        "type": "object",
        "properties": {
            "masjid_id": {
                "type": "integer",
                "description": "ID of the masjid to get prayer times for"
            }
        },
        "required": ["masjid_id"]
    },
    callable_func=DatabaseClient.get_masjid_details
)


# Tool 2: get_current_prayer
get_current_prayer = CallableTool(
    name=TOOL_GET_CURRENT_PRAYER,
    description="Gets the current or next upcoming prayer information for a specific masjid. Use this when user asks 'what's the next prayer' or 'when is the next prayer'.",
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
    callable_func=DatabaseClient.get_current_prayer
)


# Export all prayer time tools
ALL_PRAYER_TOOLS = [
    get_prayer_times,
    get_current_prayer,
]
