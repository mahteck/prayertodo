"""
Hadith MCP Tools
Tools for retrieving daily hadith and spiritual content
"""

from chatbot.mcp_tools.base import MCPTool

# Tool: Get Daily Hadith
get_daily_hadith_tool = MCPTool(
    name="get_daily_hadith",
    description="Retrieves today's hadith in both English and Urdu. The hadith includes the text and source reference. Agent should select the appropriate language field based on user's language.",
    input_schema={
        "type": "object",
        "properties": {},
        "required": []
    },
    backend_config={
        "method": "GET",
        "path": "/api/v1/hadith/today"
    }
)

# Export hadith tools
HADITH_TOOLS = [
    get_daily_hadith_tool
]


def get_hadith_tools():
    """Returns list of hadith tool schemas for OpenAI"""
    return [tool.to_openai_tool_schema() for tool in HADITH_TOOLS]
