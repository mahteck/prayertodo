"""
Base MCP Tool Class
Wraps Phase II backend APIs for use by AI agent
"""

import requests
import logging
from typing import Dict, Any, Optional, Callable
from pydantic import BaseModel
from chatbot.config.settings import BACKEND_BASE_URL

logger = logging.getLogger(__name__)


class ToolResult(BaseModel):
    """Standard result format for all MCP tools"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    error_message: Optional[str] = None

    class Config:
        extra = "allow"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return self.model_dump(exclude_none=True)


class MCPTool:
    """
    Base class for MCP tools that call Phase II backend APIs
    """

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: Dict,
        backend_config: Dict
    ):
        """
        Initialize MCP tool

        Args:
            name: Tool name for OpenAI function calling
            description: Tool description
            input_schema: JSON schema for tool inputs
            backend_config: Dict with method, path, etc.
        """
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.backend_config = backend_config

    def execute(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool by calling Phase II backend API

        Args:
            user_id: User ID for the request
            **kwargs: Tool-specific parameters

        Returns:
            API response dict or error dict
        """
        try:
            # Build URL
            url = f"{BACKEND_BASE_URL}{self.backend_config['path']}"

            # Replace path parameters (e.g., {task_id})
            for key, value in kwargs.items():
                placeholder = f"{{{key}}}"
                if placeholder in url:
                    url = url.replace(placeholder, str(value))

            # Prepare request
            method = self.backend_config['method'].upper()
            headers = {"Content-Type": "application/json"}

            # Add user_id to kwargs if not already present
            if 'user_id' not in kwargs:
                kwargs['user_id'] = user_id

            # Log the request
            logger.info(f"MCP Tool [{self.name}]: {method} {url}")
            logger.debug(f"Parameters: {kwargs}")

            # Make HTTP request
            if method == "GET":
                # For GET, use query parameters
                response = requests.get(url, params=kwargs, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=kwargs, headers=headers, timeout=10)
            elif method == "PUT":
                response = requests.put(url, json=kwargs, headers=headers, timeout=10)
            elif method == "PATCH":
                response = requests.patch(url, json=kwargs, headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, params=kwargs, headers=headers, timeout=10)
            else:
                return {"error": "INVALID_METHOD", "message": f"Unsupported HTTP method: {method}"}

            # Handle response
            if response.status_code in [200, 201]:
                result = response.json() if response.content else {"success": True}
                logger.info(f"MCP Tool [{self.name}]: Success")
                return result
            elif response.status_code == 204:
                # No content (successful DELETE)
                logger.info(f"MCP Tool [{self.name}]: Success (no content)")
                return {"success": True, "message": "Operation completed successfully"}
            elif response.status_code == 404:
                logger.warning(f"MCP Tool [{self.name}]: Resource not found")
                return {"error": "NOT_FOUND", "message": "Resource not found"}
            elif response.status_code >= 500:
                logger.error(f"MCP Tool [{self.name}]: Backend error {response.status_code}")
                return {"error": "BACKEND_ERROR", "message": "Backend service error"}
            else:
                logger.error(f"MCP Tool [{self.name}]: Error {response.status_code}")
                return {"error": "UNKNOWN_ERROR", "message": f"HTTP {response.status_code}: {response.text[:100]}"}

        except requests.exceptions.Timeout:
            logger.error(f"MCP Tool [{self.name}]: Timeout")
            return {"error": "TIMEOUT", "message": "Request timed out"}
        except requests.exceptions.ConnectionError as e:
            logger.error(f"MCP Tool [{self.name}]: Connection error: {e}")
            return {"error": "CONNECTION_ERROR", "message": f"Could not connect to backend: {str(e)}"}
        except Exception as e:
            logger.error(f"MCP Tool [{self.name}]: Unexpected error: {e}", exc_info=True)
            return {"error": "EXECUTION_ERROR", "message": f"Tool execution failed: {str(e)}"}

    def to_openai_tool_schema(self) -> Dict:
        """
        Convert this MCP tool to OpenAI function calling schema

        Returns:
            OpenAI function schema dict
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema
            }
        }


class CallableTool:
    """
    Tool wrapper for direct database access functions
    Eliminates circular HTTP dependency by calling DatabaseClient methods directly
    """

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: Dict,
        callable_func: Callable
    ):
        """
        Initialize callable tool

        Args:
            name: Tool name for OpenAI function calling
            description: Tool description
            input_schema: JSON schema for tool inputs
            callable_func: Direct function to call (e.g., DatabaseClient.create_task)
        """
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.callable_func = callable_func

    def execute(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool by calling the direct function

        Args:
            user_id: User ID for the request
            **kwargs: Tool-specific parameters

        Returns:
            ToolResult as dict
        """
        try:
            logger.info(f"CallableTool [{self.name}]: Executing for user {user_id}")
            logger.debug(f"Parameters: {kwargs}")

            # Call the function directly (bypasses HTTP)
            result = self.callable_func(user_id=user_id, **kwargs)

            # Convert ToolResult to dict if needed
            if isinstance(result, ToolResult):
                result_dict = result.to_dict()
            else:
                result_dict = result

            logger.info(f"CallableTool [{self.name}]: {'Success' if result_dict.get('success') else 'Failed'}")
            return result_dict

        except Exception as e:
            logger.error(f"CallableTool [{self.name}]: Unexpected error: {e}", exc_info=True)
            return {
                "success": False,
                "error": "EXECUTION_ERROR",
                "error_message": f"Tool execution failed: {str(e)}"
            }

    def to_openai_tool_schema(self) -> Dict:
        """
        Convert this callable tool to OpenAI function calling schema

        Returns:
            OpenAI function schema dict
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema
            }
        }
