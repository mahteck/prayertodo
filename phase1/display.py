"""
Output formatting and display functions for CLI.

This module handles all console output including banners,
help text, task tables, and detail views.
"""

from datetime import datetime
from typing import List, Optional


def show_welcome_banner() -> None:
    """Display the welcome banner on application startup."""
    print("========================================")
    print("  SalaatFlow - Prayer & Spiritual Tasks")
    print("  Phase I: Console Edition")
    print("========================================")


def show_help() -> None:
    """Display the help message with all available commands."""
    print("SalaatFlow - Prayer & Spiritual Task Manager")
    print("Available Commands:")
    print("  add              - Add a new spiritual task")
    print("  list [filter]    - List all tasks (filter: all|pending|completed)")
    print("  view <id>        - View detailed information for a task")
    print("  update <id>      - Update an existing task")
    print("  delete <id>      - Delete a task by ID")
    print("  complete <id>    - Mark a task as completed")
    print("  uncomplete <id>  - Mark a task as incomplete")
    print("  help             - Show this help message")
    print("  exit             - Exit the application")


def format_status(completed: bool) -> str:
    """
    Format completion status as checkbox.

    Args:
        completed: Whether task is completed

    Returns:
        "[✓]" if completed, "[ ]" if pending
    """
    return "[✓]" if completed else "[ ]"


def format_datetime(dt: Optional[datetime]) -> str:
    """
    Format datetime for display.

    Args:
        dt: Datetime object or None

    Returns:
        Formatted string "YYYY-MM-DD HH:MM" or "-" if None
    """
    if dt is None:
        return "-"
    return dt.strftime("%Y-%m-%d %H:%M")


def show_task_table(tasks: List[dict]) -> None:
    """
    Display tasks in a formatted table.

    Args:
        tasks: List of task dictionaries to display
    """
    if not tasks:
        print("No tasks found.")
        return

    # Print header
    print("ID | Status | Category | Title                          | Masjid           | Area         | Due Date/Time")
    print("---|--------|----------|--------------------------------|------------------|--------------|------------------")

    # Print each task
    for task in tasks:
        task_id = str(task["id"])
        status = format_status(task["completed"])
        category = task["category"]

        # Truncate title if too long
        title = task["title"]
        if len(title) > 30:
            title = title[:27] + "..."

        # Handle optional fields
        masjid = task.get("masjid_name", "") or "-"
        if len(masjid) > 16:
            masjid = masjid[:13] + "..."

        area = task.get("area_name", "") or "-"
        if len(area) > 12:
            area = area[:9] + "..."

        due = format_datetime(task.get("due_datetime"))

        # Print row with proper spacing
        print(f"{task_id:2} | {status:6} | {category:8} | {title:30} | {masjid:16} | {area:12} | {due}")

    # Print summary
    completed_count = sum(1 for task in tasks if task["completed"])
    pending_count = len(tasks) - completed_count
    print(f"\nTotal: {len(tasks)} tasks ({completed_count} completed, {pending_count} pending)")


def show_task_detail(task: dict) -> None:
    """
    Display detailed information for a single task.

    Args:
        task: Task dictionary to display
    """
    print(f"Task ID: {task['id']}")
    print(f"Title: {task['title']}")
    print(f"Description: {task.get('description', '') or '-'}")
    print(f"Category: {task['category']}")
    print(f"Masjid: {task.get('masjid_name', '') or '-'}")
    print(f"Area: {task.get('area_name', '') or '-'}")
    print(f"Due Date/Time: {format_datetime(task.get('due_datetime'))}")

    status = "Completed" if task["completed"] else "Pending"
    print(f"Status: {status}")

    print(f"Created: {format_datetime(task['created_at'])}")
    print(f"Last Updated: {format_datetime(task['updated_at'])}")
