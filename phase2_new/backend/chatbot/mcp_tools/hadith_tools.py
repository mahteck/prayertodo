"""
Hadith MCP Tools
Tools for retrieving daily and random hadith content

These tools use direct database access to avoid circular HTTP dependencies.
"""

from chatbot.mcp_tools.base import CallableTool
from chatbot.mcp_tools.db_client import DatabaseClient
from chatbot.mcp_tools.constants import (
    TOOL_GET_DAILY_HADITH,
    TOOL_GET_RANDOM_HADITH,
)


# Tool 1: get_daily_hadith
get_daily_hadith = CallableTool(
    name=TOOL_GET_DAILY_HADITH,
    description="Retrieves today's hadith in both English and Urdu. The hadith includes the text and source reference. Agent should select the appropriate language field based on user's language.",
    input_schema={
        "type": "object",
        "properties": {},
        "required": []
    },
    callable_func=DatabaseClient.get_daily_hadith
)


# Tool 2: get_random_hadith
get_random_hadith = CallableTool(
    name=TOOL_GET_RANDOM_HADITH,
    description="Retrieves a random hadith from the database in both English and Urdu. Use this when user wants to see a hadith but not specifically today's hadith.",
    input_schema={
        "type": "object",
        "properties": {},
        "required": []
    },
    callable_func=DatabaseClient.get_random_hadith
)


# Export all hadith tools
ALL_HADITH_TOOLS = [
    get_daily_hadith,
    get_random_hadith,
]
