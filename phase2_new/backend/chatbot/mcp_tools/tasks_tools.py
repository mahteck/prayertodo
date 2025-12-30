"""
Task Management MCP Tools
Simplified tool names to match agent expectations

These tools use direct database access to avoid circular HTTP dependencies.
"""

from chatbot.mcp_tools.base import CallableTool
from chatbot.mcp_tools.db_client import DatabaseClient
from chatbot.mcp_tools.constants import (
    TOOL_CREATE_TASK,
    TOOL_LIST_TASKS,
    TOOL_UPDATE_TASK,
    TOOL_DELETE_TASK,
    TOOL_COMPLETE_TASK,
)


# Tool 1: create_task
create_task = CallableTool(
    name=TOOL_CREATE_TASK,
    description="Creates a new spiritual task (prayer, deed, Quran reading, etc.) for the user. Use this when user wants to add a new task.",
    input_schema={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "ID of the user"
            },
            "title": {
                "type": "string",
                "description": "Task title/name (e.g., 'Pray Fajr at Masjid Al-Huda')"
            },
            "description": {
                "type": "string",
                "description": "Optional detailed description of the task"
            },
            "category": {
                "type": "string",
                "enum": ["Farz", "Sunnah", "Nafl", "Deed", "Other"],
                "description": "Task category: Farz (obligatory), Sunnah (prophetic tradition), Nafl (voluntary), Deed (good deeds), Other"
            },
            "priority": {
                "type": "string",
                "enum": ["high", "medium", "low"],
                "description": "Task priority level"
            },
            "masjid_id": {
                "type": "integer",
                "description": "Optional ID of associated masjid"
            },
            "due_datetime": {
                "type": "string",
                "description": "Due date and time in ISO 8601 format (e.g., '2025-12-30T05:30:00')"
            },
            "recurrence": {
                "type": "string",
                "enum": ["None", "Daily", "Weekly", "Monthly"],
                "description": "Task recurrence pattern"
            },
            "recurrence_pattern": {
                "type": "string",
                "description": "Detailed recurrence pattern (e.g., 'every_day', 'every_friday')"
            },
            "minutes_before_prayer": {
                "type": "integer",
                "description": "Minutes before prayer time for reminders"
            },
            "linked_prayer": {
                "type": "string",
                "enum": ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Jummah"],
                "description": "Prayer name this task is linked to"
            }
        },
        "required": ["user_id", "title"]
    },
    callable_func=DatabaseClient.create_task
)


# Tool 2: list_tasks
list_tasks = CallableTool(
    name=TOOL_LIST_TASKS,
    description="Lists spiritual tasks for the user with optional filters. Use this to show user their current tasks.",
    input_schema={
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "ID of the user"
            },
            "category": {
                "type": "string",
                "enum": ["Farz", "Sunnah", "Nafl", "Deed", "Other"],
                "description": "Filter by task category"
            },
            "completed": {
                "type": "boolean",
                "description": "Filter by completion status (true for completed, false for pending)"
            },
            "priority": {
                "type": "string",
                "enum": ["high", "medium", "low"],
                "description": "Filter by priority level"
            },
            "masjid_id": {
                "type": "integer",
                "description": "Filter by associated masjid"
            }
        },
        "required": ["user_id"]
    },
    callable_func=DatabaseClient.list_tasks
)


# Tool 3: update_task
update_task = CallableTool(
    name=TOOL_UPDATE_TASK,
    description="Updates an existing spiritual task. Use this to modify task details like time, priority, or description.",
    input_schema={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "ID of the task to update"
            },
            "user_id": {
                "type": "integer",
                "description": "ID of the user"
            },
            "title": {
                "type": "string",
                "description": "Updated task title"
            },
            "description": {
                "type": "string",
                "description": "Updated description"
            },
            "category": {
                "type": "string",
                "enum": ["Farz", "Sunnah", "Nafl", "Deed", "Other"],
                "description": "Updated category"
            },
            "priority": {
                "type": "string",
                "enum": ["high", "medium", "low"],
                "description": "Updated priority"
            },
            "masjid_id": {
                "type": "integer",
                "description": "Updated masjid ID"
            },
            "due_datetime": {
                "type": "string",
                "description": "Updated due date/time in ISO 8601 format"
            },
            "recurrence": {
                "type": "string",
                "enum": ["None", "Daily", "Weekly", "Monthly"],
                "description": "Updated recurrence"
            },
            "completed": {
                "type": "boolean",
                "description": "Updated completion status"
            }
        },
        "required": ["task_id", "user_id"]
    },
    callable_func=DatabaseClient.update_task
)


# Tool 4: delete_task
delete_task = CallableTool(
    name=TOOL_DELETE_TASK,
    description="Deletes a spiritual task. IMPORTANT: Always ask for confirmation before using this tool.",
    input_schema={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "ID of the task to delete"
            },
            "user_id": {
                "type": "integer",
                "description": "ID of the user"
            }
        },
        "required": ["task_id", "user_id"]
    },
    callable_func=DatabaseClient.delete_task
)


# Tool 5: complete_task
complete_task = CallableTool(
    name=TOOL_COMPLETE_TASK,
    description="Marks a spiritual task as completed. Use this when user indicates they finished a task.",
    input_schema={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "ID of the task to mark as complete"
            },
            "user_id": {
                "type": "integer",
                "description": "ID of the user"
            }
        },
        "required": ["task_id", "user_id"]
    },
    callable_func=DatabaseClient.complete_task
)


# Export all task tools
ALL_TASK_TOOLS = [
    create_task,
    list_tasks,
    update_task,
    delete_task,
    complete_task,
]
