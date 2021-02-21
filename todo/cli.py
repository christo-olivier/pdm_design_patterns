import sys
from datetime import datetime
from typing import List

from todo.model import ToDoItem
from todo.repository import CSVRepository

# Setup database and session object
db_path = "/Users/christo/repos/todo/todo_app.csv"


def _print_item(item: ToDoItem):
    """
    Print a todo item's properties to the command line.
    """
    print(
        f"Name: {item.name}, Due: {item.due}, Priority: {item.priority}, "
        f"Status: {item.status}, Completed: {item.completed}"
    )


def _get_args():
    """
    Get the arguments passed to the application from the command line.
    """
    if len(sys.argv) < 2:
        print("Please specify your command.")
        sys.exit(1)

    args = sys.argv[1:]

    return args


def show_due(due: str, items: List[ToDoItem]) -> None:
    """
    Show all of the items that are due on a specific date.
    """
    if due.lower() == "today":
        due = datetime.now().date()
    else:
        due = datetime.strptime(due, "%Y-%m-%d").date()

    for item in items:
        if item.due <= due and item.status == "active":
            _print_item(item)


def main():
    """
    Main application loop.
    """
    args = _get_args()

    # Get the command from the commandline arguments.
    command = args[0].lower()

    # Instantiate the repository
    repo = CSVRepository(db_path=db_path)

    # Execute commands
    if command == "add":
        new_item = ToDoItem(
            name=args[1],
            due=datetime.strptime(args[2], "%Y-%m-%d").date(),
            priority=args[3],
        )
        try:
            repo.add(new_item)
        except Exception as ex:
            print(ex)

    if command == "all":
        for item in repo.list():
            _print_item(item)

    if command == "complete":
        repo.mark_complete(args[1])

    if command == "due":
        show_due(args[1], repo.list())

    if command == "remove":
        repo.remove_item(args[1])

    if command == "update":
        repo.update_item(args[1], args[2], args[3])


if __name__ == "__main__":
    main()