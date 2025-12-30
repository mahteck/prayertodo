"""
Masjid MCP Tools
Tools for querying masjid information and prayer times
"""

from chatbot.mcp_tools.base import MCPTool

# Tool 1: List Masjids by Area
list_masjids_by_area_tool = MCPTool(
    name="list_masjids_by_area",
    description="Lists all masjids in a specific area. Use this when user asks about masjids in a particular location.",
    input_schema={
        "type": "object",
        "properties": {
            "area": {
                "type": "string",
                "description": "Area name (e.g., 'North Nazimabad', 'Gulshan', 'Clifton')"
            }
        },
        "required": ["area"]
    },
    backend_config={
        "method": "GET",
        "path": "/api/v1/masjids"
    }
)

# Tool 2: Search Masjid by Name
search_masjid_by_name_tool = MCPTool(
    name="search_masjid_by_name",
    description="Searches for masjids by name, optionally filtered by area. Use this to find a specific masjid.",
    input_schema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Masjid name or partial name to search for"
            },
            "area": {
                "type": "string",
                "description": "Optional area name to filter results"
            }
        },
        "required": ["name"]
    },
    backend_config={
        "method": "GET",
        "path": "/api/v1/masjids"
    }
)

# Tool 3: Get Masjid Details
get_masjid_details_tool = MCPTool(
    name="get_masjid_details",
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
    backend_config={
        "method": "GET",
        "path": "/api/v1/masjids/{masjid_id}"
    }
)

# Tool 4: Get Prayer Time (implemented via get_masjid_details + extraction)
# This is a composite tool that uses get_masjid_details and extracts specific prayer
get_prayer_time_tool = MCPTool(
    name="get_prayer_time",
    description="Gets a specific prayer time for a masjid. Use this when user asks 'what time is Fajr at...' etc.",
    input_schema={
        "type": "object",
        "properties": {
            "masjid_id": {
                "type": "integer",
                "description": "ID of the masjid"
            },
            "prayer_name": {
                "type": "string",
                "enum": ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"],
                "description": "Name of the prayer"
            }
        },
        "required": ["masjid_id", "prayer_name"]
    },
    backend_config={
        "method": "GET",
        "path": "/api/v1/masjids/{masjid_id}"
    }
)

# Export all masjid tools
MASJID_TOOLS = [
    list_masjids_by_area_tool,
    search_masjid_by_name_tool,
    get_masjid_details_tool,
    get_prayer_time_tool
]


def get_masjid_tools():
    """Returns list of masjid tool schemas for OpenAI"""
    return [tool.to_openai_tool_schema() for tool in MASJID_TOOLS]
