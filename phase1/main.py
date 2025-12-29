"""
SalaatFlow - Prayer & Spiritual Task Manager
Phase I: In-Memory Python Console Application

Main entry point for the application.
"""

from typing import List

try:
    from storage import TaskStorage
    from display import show_welcome_banner, show_help
    from commands import (
        handle_help, handle_add, handle_list, handle_view,
        handle_update, handle_delete, handle_complete, handle_uncomplete
    )
except ImportError:
    from phase1.storage import TaskStorage
    from phase1.display import show_welcome_banner, show_help
    from phase1.commands import (
        handle_help, handle_add, handle_list, handle_view,
        handle_update, handle_delete, handle_complete, handle_uncomplete
    )


def parse_command(user_input: str) -> tuple[str, List[str]]:
    """
    Parse user input into command and arguments.

    Args:
        user_input: Raw input string from user

    Returns:
        Tuple of (command, arguments_list)
    """
    if not user_input or not user_input.strip():
        return ("", [])

    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []

    return (command, args)


def dispatch_command(cmd: str, args: List[str], storage: TaskStorage) -> bool:
    """
    Dispatch command to appropriate handler.

    Args:
        cmd: Command name
        args: Command arguments
        storage: TaskStorage instance

    Returns:
        True to continue REPL loop, False to exit
    """
    if not cmd:
        # Empty command, just continue
        return True

    if cmd == "help":
        handle_help(storage)
    elif cmd == "add":
        handle_add(storage)
    elif cmd == "list":
        handle_list(storage, args)
    elif cmd == "view":
        handle_view(storage, args)
    elif cmd == "update":
        handle_update(storage, args)
    elif cmd == "delete":
        handle_delete(storage, args)
    elif cmd == "complete":
        handle_complete(storage, args)
    elif cmd == "uncomplete":
        handle_uncomplete(storage, args)
    elif cmd == "exit":
        return False  # Signal to exit
    else:
        print(f"Error: Unknown command '{cmd}'. Type 'help' for available commands.")

    return True  # Continue loop


def main() -> None:
    """Main application entry point."""
    # Initialize storage
    storage = TaskStorage()

    # Display welcome banner and help
    show_welcome_banner()
    print()
    show_help()
    print()

    # Main REPL loop
    try:
        while True:
            # Display prompt
            user_input = input("salaatflow> ")

            # Parse command
            cmd, args = parse_command(user_input)

            # Dispatch command
            should_continue = dispatch_command(cmd, args, storage)

            if not should_continue:
                break

            print()  # Blank line between commands

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n")

    # Display farewell message
    print("JazakAllah Khair for using SalaatFlow! May your deeds be accepted.")


if __name__ == "__main__":
    main()
