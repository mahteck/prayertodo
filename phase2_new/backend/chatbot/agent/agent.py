"""
Google Gemini Agent Implementation - Simplified Version
Core logic for SalaatFlow AI Assistant using Google Gemini API (FREE)
Uses simple conversation mode with manual intent detection for tool calling
"""

import json
import logging
import re
from typing import List, Dict, Optional

from chatbot.agent.config import AGENT_CONFIG
from chatbot.agent.prompts import SYSTEM_PROMPT
from chatbot.mcp_tools import execute_tool

logger = logging.getLogger(__name__)


def initialize_agent():
    """
    Initialize Google Gemini model for simple conversation

    Returns:
        None (agent initialization now handled by GeminiClient)

    Note: This function is kept for backward compatibility but is no longer needed.
    The GeminiClient is now initialized in the router's startup event.
    """
    logger.info("Agent initialization is now handled by GeminiClient")
    return None


def detect_intent(user_message: str) -> Dict[str, any]:
    """
    Detect user intent from message using keyword matching

    Args:
        user_message: User's message

    Returns:
        Dict with intent type and extracted parameters
    """
    msg_lower = user_message.lower()

    # Task creation patterns
    create_patterns = [
        r'task\s+(create|bana|add|new)',
        r'(bana|create|add)\s+.*task',
        r'namaz.*task',
        r'(fajr|dhuhr|asr|maghrib|isha).*task',
    ]

    # Task update patterns
    update_patterns = [
        r'task\s+(update|edit|change|modify)',
        r'(complete|done|finish).*task',
        r'urgent.*task',
        r'task.*urgent',
    ]

    # Task deletion patterns
    delete_patterns = [
        r'task\s+(delete|remove|cancel)',
        r'(delete|remove|cancel).*task',
    ]

    # Task list patterns
    list_patterns = [
        r'(show|display|list|dikhao).*task',
        r'task.*list',
        r'mery\s+task',
        r'konse\s+task',
    ]

    # Masjid search patterns
    masjid_patterns = [
        r'masjid.*search',
        r'konsi\s+masjid',
        r'masjid.*area',
        r'namaz.*kahan',
    ]

    # Check each pattern type
    for pattern in create_patterns:
        if re.search(pattern, msg_lower):
            return {"intent": "create_task", "message": user_message}

    for pattern in update_patterns:
        if re.search(pattern, msg_lower):
            return {"intent": "update_task", "message": user_message}

    for pattern in delete_patterns:
        if re.search(pattern, msg_lower):
            return {"intent": "delete_task", "message": user_message}

    for pattern in list_patterns:
        if re.search(pattern, msg_lower):
            return {"intent": "list_tasks", "message": user_message}

    for pattern in masjid_patterns:
        if re.search(pattern, msg_lower):
            return {"intent": "search_masjids", "message": user_message}

    return {"intent": "conversation", "message": user_message}


def extract_task_params(user_message: str, intent_type: str) -> Dict[str, any]:
    """
    Extract task parameters from user message

    Args:
        user_message: User's message
        intent_type: Type of intent detected

    Returns:
        Dict with extracted parameters
    """
    params = {}
    msg_lower = user_message.lower()

    # Extract prayer names
    prayers = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']
    for prayer in prayers:
        if prayer in msg_lower:
            params['linked_prayer'] = prayer.capitalize()
            break

    # Extract priority keywords
    if any(word in msg_lower for word in ['urgent', 'zaruri', 'important']):
        params['priority'] = 'high'
    elif any(word in msg_lower for word in ['low', 'kam']):
        params['priority'] = 'low'
    else:
        params['priority'] = 'medium'

    # Extract time patterns
    time_match = re.search(r'(\d{1,2}):(\d{2})', user_message)
    if time_match:
        params['time'] = f"{time_match.group(1)}:{time_match.group(2)}"

    # Extract task title (for creation)
    if intent_type == "create_task":
        # Remove common trigger words to get title
        title = user_message
        for word in ['task', 'bana', 'create', 'add', 'do', 'kr', 'ka', 'ki']:
            title = re.sub(rf'\b{word}\b', '', title, flags=re.IGNORECASE)
        params['title'] = title.strip()

    return params


def run_agent(
    agent,
    user_id: int,
    user_message: str,
    conversation_history: Optional[List[Dict]] = None,
    gemini_client=None,
    request_id: Optional[str] = None
) -> str:
    """
    Run the Gemini agent with manual intent detection and tool calling

    Args:
        agent: Deprecated - no longer used (kept for backward compatibility)
        user_id: User ID for tool executions
        user_message: The user's message
        conversation_history: Optional list of previous messages
        gemini_client: GeminiClient instance for API calls
        request_id: Optional request ID for logging and tracking

    Returns:
        Assistant's response message

    Raises:
        GeminiAuthError: If API authentication fails
        GeminiQuotaError: If API quota is exceeded
        GeminiNetworkError: If network error occurs
        GeminiError: For other Gemini API errors
    """
    log_extra = {"request_id": request_id} if request_id else {}

    logger.info(
        f"Running Gemini agent for user {user_id}: {user_message[:50]}...",
        extra=log_extra
    )

    # Detect user intent first
    intent_data = detect_intent(user_message)
    intent = intent_data["intent"]

    logger.info(f"Detected intent: {intent}", extra=log_extra)

    # Handle task operations with direct tool calling
    if intent == "create_task":
        params = extract_task_params(user_message, intent)
        logger.info(f"Creating task with params: {params}", extra=log_extra)

        # Call create_task tool directly
        result = execute_tool(
            "create_task",
            user_id,
            title=params.get('title', 'New Task'),
            description=user_message,
            priority=params.get('priority', 'medium'),
            linked_prayer=params.get('linked_prayer')
        )

        if result.get('success'):
            task = result.get('task', {})
            return f"✅ Task created successfully!\n\nTitle: {task.get('title')}\nPriority: {task.get('priority')}\nLinked Prayer: {task.get('linked_prayer', 'None')}"
        else:
            return f"❌ Failed to create task: {result.get('error', 'Unknown error')}"

    elif intent == "list_tasks":
        logger.info("Listing tasks for user", extra=log_extra)
        result = execute_tool("list_tasks", user_id)

        if result.get('success'):
            tasks = result.get('tasks', [])
            if not tasks:
                return "You don't have any tasks yet. Would you like to create one?"

            response = f"📋 Your Tasks ({len(tasks)} total):\n\n"
            for i, task in enumerate(tasks, 1):
                status = "✅" if task.get('completed') else "⏳"
                prayer = f" ({task.get('linked_prayer')})" if task.get('linked_prayer') else ""
                response += f"{i}. {status} {task.get('title')}{prayer}\n   Priority: {task.get('priority')}\n\n"

            return response
        else:
            return f"❌ Failed to fetch tasks: {result.get('error', 'Unknown error')}"

    elif intent == "update_task":
        # For now, ask user for task ID
        return "To update a task, please provide the task number or title you want to update."

    elif intent == "delete_task":
        # For now, ask user for task ID
        return "To delete a task, please provide the task number or title you want to delete."

    elif intent == "search_masjids":
        # Extract area from message
        area_match = re.search(r'(North Nazimabad|DHA|Clifton|Gulshan|Malir)', user_message, re.IGNORECASE)
        area = area_match.group(1) if area_match else None

        result = execute_tool("search_masjids", user_id, area=area)

        if result.get('success'):
            masjids = result.get('masjids', [])
            if not masjids:
                return f"No masjids found{' in ' + area if area else ''}."

            response = f"🕌 Found {len(masjids)} masjid(s){' in ' + area if area else ''}:\n\n"
            for i, masjid in enumerate(masjids, 1):
                response += f"{i}. {masjid.get('name')}\n"
                response += f"   Area: {masjid.get('area_name')}, {masjid.get('city')}\n"
                response += f"   Fajr: {masjid.get('fajr_time')} | Dhuhr: {masjid.get('dhuhr_time')}\n\n"

            return response
        else:
            return f"❌ Failed to search masjids: {result.get('error', 'Unknown error')}"

    # For general conversation, use Gemini
    else:
        if gemini_client is None:
            logger.error("GeminiClient not provided to agent", extra=log_extra)
            raise ValueError("GeminiClient is required for conversation mode")

        # Build conversation context for Gemini
        conversation_context = ""
        if conversation_history:
            for msg in conversation_history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                conversation_context += f"{role.upper()}: {content}\n"
            conversation_context += f"USER: {user_message}\n"
        else:
            conversation_context = user_message

        # Use GeminiClient to generate response
        logger.debug(
            f"Generating response with GeminiClient",
            extra=log_extra
        )

        response_text = gemini_client.generate_response(
            prompt=conversation_context,
            system_instruction=SYSTEM_PROMPT,
            context={"request_id": request_id, "user_id": user_id}
        )

        logger.info(
            f"Gemini response generated: {len(response_text)} chars",
            extra=log_extra
        )

        return response_text


def cleanup_agent():
    """
    Cleanup agent resources (not needed for Gemini)
    """
    logger.info("Gemini model is stateless, no cleanup needed")
