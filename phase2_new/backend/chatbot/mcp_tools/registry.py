"""
MCP Tools Registry
Central registry for all MCP tools - ensures tools are available and can be executed

CRITICAL: This registry MUST contain all 12 tools defined in constants.py.
Application startup MUST fail if any tool is missing.
"""

import logging
from typing import Dict, Any, List, Optional

from chatbot.mcp_tools.constants import ALL_TOOL_NAMES, get_tool_category
from chatbot.mcp_tools.tasks_tools import ALL_TASK_TOOLS
from chatbot.mcp_tools.masjid_tools import ALL_MASJID_TOOLS
from chatbot.mcp_tools.prayer_tools import ALL_PRAYER_TOOLS
from chatbot.mcp_tools.hadith_tools import ALL_HADITH_TOOLS

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Central registry for all MCP tools

    Responsibilities:
    - Store all available tools
    - Execute tools by name
    - Validate tool availability
    - Report missing tools
    """

    def __init__(self):
        """Initialize the tool registry"""
        self._tools: Dict[str, Any] = {}
        self._register_all_tools()

    def _register_all_tools(self):
        """
        Register all tools from all categories

        Raises:
            RuntimeError: If duplicate tool names are found
        """
        all_tools = (
            ALL_TASK_TOOLS +
            ALL_MASJID_TOOLS +
            ALL_PRAYER_TOOLS +
            ALL_HADITH_TOOLS
        )

        for tool in all_tools:
            if tool.name in self._tools:
                raise RuntimeError(
                    f"Duplicate tool name '{tool.name}' detected. "
                    f"Tool names must be unique."
                )

            self._tools[tool.name] = tool
            logger.debug(f"Registered tool: {tool.name} (category: {get_tool_category(tool.name)})")

        logger.info(f"✅ Tool registry initialized with {len(self._tools)} tools")

    def has(self, tool_name: str) -> bool:
        """
        Check if a tool is registered

        Args:
            tool_name: Name of the tool to check

        Returns:
            True if tool is registered, False otherwise
        """
        return tool_name in self._tools

    def get(self, tool_name: str) -> Optional[Any]:
        """
        Get a tool by name

        Args:
            tool_name: Name of the tool to retrieve

        Returns:
            Tool object if found, None otherwise
        """
        return self._tools.get(tool_name)

    def execute(self, tool_name: str, user_id: int, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool by name

        Args:
            tool_name: Name of the tool to execute
            user_id: User ID for the request
            **kwargs: Tool-specific parameters

        Returns:
            Tool execution result

        Raises:
            ToolNotFoundError: If tool is not in registry
        """
        if tool_name not in self._tools:
            error_msg = f"Tool '{tool_name}' not found in registry"
            logger.error(error_msg)
            return {
                "success": False,
                "error": "TOOL_NOT_FOUND",
                "error_message": error_msg,
                "available_tools": list(self._tools.keys())
            }

        tool = self._tools[tool_name]
        logger.info(f"Executing tool: {tool_name} for user {user_id}")

        try:
            result = tool.execute(user_id, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Tool execution error: {tool_name} - {e}", exc_info=True)
            return {
                "success": False,
                "error": "TOOL_EXECUTION_ERROR",
                "error_message": f"Failed to execute tool '{tool_name}': {str(e)}"
            }

    def get_all_tool_names(self) -> List[str]:
        """
        Get list of all registered tool names

        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def get_missing_tools(self) -> List[str]:
        """
        Get list of tools that are required but not registered

        Returns:
            List of missing tool names
        """
        registered = set(self._tools.keys())
        required = set(ALL_TOOL_NAMES)
        missing = required - registered
        return list(missing)

    def validate(self) -> bool:
        """
        Validate that all required tools are registered

        Returns:
            True if all tools are registered, False otherwise
        """
        missing = self.get_missing_tools()

        if missing:
            logger.error(f"❌ Missing tools in registry: {missing}")
            return False

        if len(self._tools) != len(ALL_TOOL_NAMES):
            logger.warning(
                f"⚠️ Tool count mismatch: "
                f"expected {len(ALL_TOOL_NAMES)}, got {len(self._tools)}"
            )
            return False

        logger.info(f"✅ Tool registry validation passed: all {len(ALL_TOOL_NAMES)} tools registered")
        return True

    def get_tools_by_category(self, category: str) -> List[str]:
        """
        Get all tools in a specific category

        Args:
            category: Category name (task_management, masjid, prayer, hadith)

        Returns:
            List of tool names in that category
        """
        return [
            tool_name
            for tool_name in self._tools.keys()
            if get_tool_category(tool_name) == category
        ]


# Global registry instance
_global_registry: Optional[ToolRegistry] = None


def get_tool_registry() -> ToolRegistry:
    """
    Get the global tool registry instance (singleton pattern)

    Returns:
        ToolRegistry instance
    """
    global _global_registry

    if _global_registry is None:
        _global_registry = ToolRegistry()

    return _global_registry


def execute_tool(tool_name: str, user_id: int, **kwargs) -> Dict[str, Any]:
    """
    Execute a tool by name using the global registry

    Args:
        tool_name: Name of the tool to execute
        user_id: User ID for the request
        **kwargs: Tool-specific parameters

    Returns:
        Tool execution result
    """
    registry = get_tool_registry()
    return registry.execute(tool_name, user_id, **kwargs)


def validate_all_tools() -> bool:
    """
    Validate that all required tools are registered in the global registry

    Returns:
        True if all tools are registered, False otherwise

    Raises:
        RuntimeError: If validation fails and application should not start
    """
    registry = get_tool_registry()

    if not registry.validate():
        missing = registry.get_missing_tools()
        raise RuntimeError(
            f"CRITICAL: MCP Tool Registry validation failed. "
            f"Missing tools: {missing}. "
            f"Expected {len(ALL_TOOL_NAMES)} tools, got {len(registry.get_all_tool_names())}. "
            f"Application cannot start without all tools registered."
        )

    return True
