"""
Spiritual Task MCP Tools
Tools for managing spiritual tasks via AI agent
"""

from chatbot.mcp_tools.base import MCPTool

# Tool 1: Create Spiritual Task
create_task_tool = MCPTool(
    name="create_spiritual_task",
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
                "enum": ["High", "Medium", "Low"],
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
        "required": ["user_id", "title", "category", "priority"]
    },
    backend_config={
        "method": "POST",
        "path": "/api/v1/tasks"
    }
)

# Tool 2: List Spiritual Tasks
list_tasks_tool = MCPTool(
    name="list_spiritual_tasks",
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
                "enum": ["High", "Medium", "Low"],
                "description": "Filter by priority level"
            },
            "masjid_id": {
                "type": "integer",
                "description": "Filter by associated masjid"
            }
        },
        "required": ["user_id"]
    },
    backend_config={
        "method": "GET",
        "path": "/api/v1/tasks"
    }
)

# Tool 3: Update Spiritual Task
update_task_tool = MCPTool(
    name="update_spiritual_task",
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
                "enum": ["High", "Medium", "Low"],
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
    backend_config={
        "method": "PUT",
        "path": "/api/v1/tasks/{task_id}"
    }
)

# Tool 4: Complete Spiritual Task
complete_task_tool = MCPTool(
    name="complete_spiritual_task",
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
    backend_config={
        "method": "PATCH",
        "path": "/api/v1/tasks/{task_id}/complete"
    }
)

# Tool 5: Uncomplete Spiritual Task
uncomplete_task_tool = MCPTool(
    name="uncomplete_spiritual_task",
    description="Marks a spiritual task as not completed. Use this when user wants to reopen a task.",
    input_schema={
        "type": "object",
        "properties": {
            "task_id": {
                "type": "integer",
                "description": "ID of the task to mark as incomplete"
            },
            "user_id": {
                "type": "integer",
                "description": "ID of the user"
            }
        },
        "required": ["task_id", "user_id"]
    },
    backend_config={
        "method": "PATCH",
        "path": "/api/v1/tasks/{task_id}/incomplete"
    }
)

# Tool 6: Delete Spiritual Task
delete_task_tool = MCPTool(
    name="delete_spiritual_task",
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
    backend_config={
        "method": "DELETE",
        "path": "/api/v1/tasks/{task_id}"
    }
)

# Export all task tools
TASK_TOOLS = [
    create_task_tool,
    list_tasks_tool,
    update_task_tool,
    complete_task_tool,
    uncomplete_task_tool,
    delete_task_tool
]


def get_task_tools():
    """Returns list of task tool schemas for OpenAI"""
    return [tool.to_openai_tool_schema() for tool in TASK_TOOLS]
