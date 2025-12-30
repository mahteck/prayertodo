"""
Agent Configuration
Settings for OpenAI Agents SDK
"""

from chatbot.config.settings import (
    CHATBOT_MODEL,
    CHATBOT_TEMPERATURE,
    CHATBOT_MAX_TOKENS,
    CHATBOT_TIMEOUT
)

# Agent configuration dictionary
AGENT_CONFIG = {
    "model": CHATBOT_MODEL,
    "temperature": CHATBOT_TEMPERATURE,
    "max_tokens": CHATBOT_MAX_TOKENS,
    "max_tool_calls": 10,  # Prevent infinite loops
    "max_recursion_depth": 5,  # Limit nested tool calls
    "timeout": CHATBOT_TIMEOUT,
}
