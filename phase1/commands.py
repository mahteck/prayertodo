"""
Command handlers for CLI operations.

This module implements all command handlers for the SalaatFlow
console application including add, list, view, update, delete, etc.
"""

from typing import List, Optional
from datetime import datetime

try:
    from storage import TaskStorage
    from display import show_help, show_task_table, show_task_detail
    from validators import validate_id, validate_title, validate_category, validate_datetime
    from models import CATEGORIES
except ImportError:
    from phase1.storage import TaskStorage
    from phase1.display import show_help, show_task_table, show_task_detail
    from phase1.validators import validate_id, validate_title, validate_category, validate_datetime
    from phase1.models import CATEGORIES


def handle_help(storage: TaskStorage) -> None:
    """
    Display help message.

    Args:
        storage: TaskStorage instance (unused but kept for consistency)
    """
    show_help()


def handle_list(storage: TaskStorage, args: List[str]) -> None:
    """
    List tasks with optional filtering.

    Args:
        storage: TaskStorage instance
        args: Command arguments (optional filter: all/pending/completed)
    """
    # Parse filter argument (default to "all")
    filter_type = "all"
    if args:
        filter_type = args[0].lower()

    # Validate filter
    if filter_type not in ["all", "pending", "completed"]:
        print("Error: Invalid filter. Use: all, pending, or completed")
        return

    # Get filtered tasks
    tasks = storage.list_tasks(filter_type)

    # Display results
    if not tasks:
        if filter_type == "all":
            print("No tasks found.")
        else:
            print(f"No tasks found matching filter: {filter_type}")
    else:
        show_task_table(tasks)


def handle_view(storage: TaskStorage, args: List[str]) -> None:
    """
    View detailed information for a single task.

    Args:
        storage: TaskStorage instance
        args: Command arguments (requires task ID)
    """
    # Check if ID argument provided
    if not args:
        print("Error: Command 'view' requires argument(s). Usage: view <id>")
        return

    # Validate ID
    is_valid, task_id = validate_id(args[0])
    if not is_valid:
        print("Error: Invalid task ID. Please enter a number.")
        return

    # Get task
    task = storage.get_task(task_id)
    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Display task details
    show_task_detail(task)


def prompt_category() -> str:
    """
    Prompt user to select a category.

    Returns:
        Selected category name (Farz, Sunnah, Nafl, or Deed)
    """
    while True:
        print("Select category:")
        for i, category in enumerate(CATEGORIES, 1):
            print(f"  {i}. {category}")

        choice = input("Enter choice (1-4): ").strip()

        is_valid, category = validate_category(choice)
        if is_valid:
            return category

        print("Invalid choice. Please enter a number between 1 and 4.")


def prompt_datetime() -> Optional[datetime]:
    """
    Prompt user for a datetime input.

    Returns:
        Datetime object if valid input, None if skipped or invalid after retries
    """
    while True:
        user_input = input("Enter due date/time (optional, format: YYYY-MM-DD HH:MM or press Enter to skip): ").strip()

        # Allow skipping
        if not user_input:
            return None

        is_valid, dt = validate_datetime(user_input)
        if is_valid:
            return dt

        print("Invalid format. Please use YYYY-MM-DD HH:MM format (e.g., 2025-12-28 05:30)")
        # Allow user to skip after error
        retry = input("Try again? (y/n): ").strip().lower()
        if retry != 'y':
            return None


def prompt_for_task_data() -> dict:
    """
    Prompt user for all task fields interactively.

    Returns:
        Dictionary with user-provided task data (no id, timestamps, or completed flag)
    """
    # Prompt for title (required)
    while True:
        title = input("Enter task title (required): ").strip()
        is_valid, error_msg = validate_title(title)
        if is_valid:
            break
        print(f"Error: {error_msg}")

    # Prompt for description (optional)
    description = input("Enter description (optional, press Enter to skip): ").strip()

    # Prompt for category
    category = prompt_category()

    # Prompt for masjid (optional)
    masjid_name = input("Enter masjid name (optional): ").strip()

    # Prompt for area (optional)
    area_name = input("Enter area name (optional): ").strip()

    # Prompt for due datetime (optional)
    due_datetime = prompt_datetime()

    return {
        "title": title,
        "description": description,
        "category": category,
        "masjid_name": masjid_name,
        "area_name": area_name,
        "due_datetime": due_datetime
    }


def handle_add(storage: TaskStorage) -> None:
    """
    Add a new task interactively.

    Args:
        storage: TaskStorage instance
    """
    # Get task data from user
    task_data = prompt_for_task_data()

    # Add auto-generated fields
    task_data["created_at"] = datetime.now()
    task_data["updated_at"] = datetime.now()
    task_data["completed"] = False

    # Add to storage
    task_id = storage.add_task(task_data)

    print(f"\nTask added successfully! (ID: {task_id})")


def prompt_for_update_data(current_task: dict) -> dict:
    """
    Prompt user for updated task fields, allowing them to keep current values.

    Args:
        current_task: The current task dictionary

    Returns:
        Dictionary with only changed fields
    """
    updates = {}

    # Prompt for title
    print(f"Current title: {current_task['title']}")
    new_title = input("New title (press Enter to keep current): ").strip()
    if new_title:
        is_valid, error_msg = validate_title(new_title)
        if is_valid:
            updates["title"] = new_title
        else:
            print(f"Error: {error_msg}. Keeping current title.")

    # Prompt for description
    current_desc = current_task.get('description', '') or '-'
    print(f"Current description: {current_desc}")
    new_desc = input("New description (press Enter to keep current): ").strip()
    if new_desc:
        updates["description"] = new_desc

    # Prompt for category
    print(f"Current category: {current_task['category']}")
    print("Select new category (press Enter to keep current):")
    for i, category in enumerate(CATEGORIES, 1):
        print(f"  {i}. {category}")
    choice = input("Enter choice (1-4) or press Enter: ").strip()
    if choice:
        is_valid, category = validate_category(choice)
        if is_valid:
            updates["category"] = category
        else:
            print("Invalid choice. Keeping current category.")

    # Prompt for masjid
    current_masjid = current_task.get('masjid_name', '') or '-'
    print(f"Current masjid: {current_masjid}")
    new_masjid = input("New masjid (press Enter to keep current): ").strip()
    if new_masjid:
        updates["masjid_name"] = new_masjid

    # Prompt for area
    current_area = current_task.get('area_name', '') or '-'
    print(f"Current area: {current_area}")
    new_area = input("New area (press Enter to keep current): ").strip()
    if new_area:
        updates["area_name"] = new_area

    # Prompt for due datetime
    from display import format_datetime
    current_due = format_datetime(current_task.get('due_datetime'))
    print(f"Current due date/time: {current_due}")
    new_due_str = input("New due date/time (format: YYYY-MM-DD HH:MM, press Enter to keep current): ").strip()
    if new_due_str:
        is_valid, new_due = validate_datetime(new_due_str)
        if is_valid:
            updates["due_datetime"] = new_due
        else:
            print("Invalid format. Keeping current due date/time.")

    return updates


def handle_update(storage: TaskStorage, args: List[str]) -> None:
    """
    Update an existing task interactively.

    Args:
        storage: TaskStorage instance
        args: Command arguments (requires task ID)
    """
    # Check if ID argument provided
    if not args:
        print("Error: Command 'update' requires argument(s). Usage: update <id>")
        return

    # Validate ID
    is_valid, task_id = validate_id(args[0])
    if not is_valid:
        print("Error: Invalid task ID. Please enter a number.")
        return

    # Get task
    task = storage.get_task(task_id)
    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Show current task
    print(f"\nUpdating Task ID: {task_id}\n")

    # Get updates from user
    updates = prompt_for_update_data(task)

    # Add updated timestamp
    updates["updated_at"] = datetime.now()

    # Apply updates
    storage.update_task(task_id, updates)

    print("\nTask updated successfully!")


def confirm_deletion(task: dict) -> bool:
    """
    Prompt user to confirm task deletion.

    Args:
        task: Task dictionary to delete

    Returns:
        True if user confirms, False otherwise
    """
    print("Are you sure you want to delete this task?")
    print(f"  ID: {task['id']}")
    print(f"  Title: {task['title']}")

    confirmation = input("Confirm deletion? (y/n): ").strip().lower()
    return confirmation == 'y'


def handle_delete(storage: TaskStorage, args: List[str]) -> None:
    """
    Delete a task after confirmation.

    Args:
        storage: TaskStorage instance
        args: Command arguments (requires task ID)
    """
    # Check if ID argument provided
    if not args:
        print("Error: Command 'delete' requires argument(s). Usage: delete <id>")
        return

    # Validate ID
    is_valid, task_id = validate_id(args[0])
    if not is_valid:
        print("Error: Invalid task ID. Please enter a number.")
        return

    # Get task
    task = storage.get_task(task_id)
    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Confirm deletion
    if confirm_deletion(task):
        storage.delete_task(task_id)
        print("\nTask deleted successfully!")
    else:
        print("\nDeletion cancelled.")


def handle_complete(storage: TaskStorage, args: List[str]) -> None:
    """
    Mark a task as completed.

    Args:
        storage: TaskStorage instance
        args: Command arguments (requires task ID)
    """
    # Check if ID argument provided
    if not args:
        print("Error: Command 'complete' requires argument(s). Usage: complete <id>")
        return

    # Validate ID
    is_valid, task_id = validate_id(args[0])
    if not is_valid:
        print("Error: Invalid task ID. Please enter a number.")
        return

    # Get task
    task = storage.get_task(task_id)
    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Check if already completed
    if task["completed"]:
        print(f"Task ID {task_id} is already completed.")
        return

    # Mark as completed
    storage.update_task(task_id, {
        "completed": True,
        "updated_at": datetime.now()
    })

    print(f"Task ID {task_id} marked as completed!")


def handle_uncomplete(storage: TaskStorage, args: List[str]) -> None:
    """
    Mark a task as incomplete.

    Args:
        storage: TaskStorage instance
        args: Command arguments (requires task ID)
    """
    # Check if ID argument provided
    if not args:
        print("Error: Command 'uncomplete' requires argument(s). Usage: uncomplete <id>")
        return

    # Validate ID
    is_valid, task_id = validate_id(args[0])
    if not is_valid:
        print("Error: Invalid task ID. Please enter a number.")
        return

    # Get task
    task = storage.get_task(task_id)
    if task is None:
        print(f"Error: Task with ID {task_id} not found.")
        return

    # Check if already incomplete
    if not task["completed"]:
        print(f"Task ID {task_id} is already incomplete.")
        return

    # Mark as incomplete
    storage.update_task(task_id, {
        "completed": False,
        "updated_at": datetime.now()
    })

    print(f"Task ID {task_id} marked as incomplete!")
