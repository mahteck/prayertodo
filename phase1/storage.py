"""
In-memory storage manager for spiritual tasks.

This module provides the TaskStorage class for CRUD operations
on tasks stored in memory (not persisted to disk).
"""

from typing import List, Optional


class TaskStorage:
    """
    In-memory storage for spiritual tasks.

    Manages a list of task dictionaries with auto-incrementing IDs.
    """

    def __init__(self):
        """Initialize empty storage."""
        self.tasks: List[dict] = []
        self.next_id: int = 1

    def add_task(self, task: dict) -> int:
        """
        Add a new task to storage.

        Args:
            task: Task dictionary (without ID)

        Returns:
            The assigned task ID
        """
        task["id"] = self.next_id
        self.tasks.append(task)
        assigned_id = self.next_id
        self.next_id += 1
        return assigned_id

    def get_task(self, task_id: int) -> Optional[dict]:
        """
        Retrieve a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task dictionary if found, None otherwise
        """
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def update_task(self, task_id: int, updates: dict) -> bool:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            updates: Dictionary of fields to update

        Returns:
            True if task found and updated, False otherwise
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        # Update fields
        for key, value in updates.items():
            task[key] = value

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task found and deleted, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                return True
        return False

    def list_tasks(self, filter: str = "all") -> List[dict]:
        """
        List tasks with optional filtering.

        Args:
            filter: Filter type - "all", "pending", or "completed"

        Returns:
            List of task dictionaries matching the filter
        """
        if filter == "all":
            return self.tasks.copy()
        elif filter == "pending":
            return [task for task in self.tasks if not task["completed"]]
        elif filter == "completed":
            return [task for task in self.tasks if task["completed"]]
        else:
            return self.tasks.copy()  # Default to all if invalid filter
