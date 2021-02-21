import sys
from datetime import date, datetime

from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from todo.data import Base, Item

db_path = "/Users/christo/repos/todo/todo_app.sqlite"
engine = engine.create_engine(f"sqlite:///{db_path}")
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)

session = DBSession()


def _convert_to_date(date_str: str):
    """
    Convert dates in string format to python date objects.
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def _print_item(item: Item):
    """
    Print a todo item's properties to the command line.
    """
    print(
        f"Name: {item.name}, Due: {item.due}, Priority: {item.priority},"
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


def add_item(name: str, due: str, priority: str) -> None:
    """
    Add a todo item to the database.
    """
    try:
        new_todo = Item(name=name, due=_convert_to_date(due), priority=priority.lower())
        session.add(new_todo)
        session.commit()
    except IntegrityError:
        print("Todo item already exists.")
        session.rollback()


def mark_complete(name: str) -> None:
    """
    Mark a todo item as completed.
    """
    item = session.query(Item).filter(Item.name == name).first()

    if not item:
        print("No todo item with name `{name}` found.")

    item.status = "complete"
    item.completed = datetime.now().date()
    session.commit()


def remove_item(name: str) -> None:
    """
    Remove a todo item from the database.
    """
    item = session.query(Item).filter(Item.name == name).first()

    if not item:
        print(f"No todo item with name `{name}` found.")
        return

    session.delete(item)
    session.commit()


def show_all() -> None:
    """
    Show all of the items in the database.
    """
    items = session.query(Item).all()
    for item in items:
        _print_item(item)


def show_due(due: str) -> None:
    """
    Show all of the items that are due on a specific date.
    """
    if due.lower() == "today":
        due = datetime.now().date()
    else:
        due = _convert_to_date(due)

    items = session.query(Item).filter(Item.due <= due)
    for item in items:
        _print_item(item)


def update_item(name: str, due: str, priority: str) -> None:
    """
    Update an item's properties.
    """
    try:
        item = session.query(Item).filter_by(name=name).first()
        item.due = _convert_to_date(due)
        item.priority = priority
        session.commit()
    except AttributeError:
        print(f"No todo item with name `{name}` found.")


def main():
    """
    Main application loop.
    """
    args = _get_args()

    # Get the command from the commandline arguments.
    command = args[0].lower()

    # Execute commands
    if command == "add":
        add_item(args[1], args[2], args[3])

    if command == "all":
        show_all()

    if command == "complete":
        mark_complete(args[1])

    if command == "due":
        show_due(args[1])

    if command == "remove":
        remove_item(args[1])

    if command == "update":
        update_item(args[1], args[2], args[3])


if __name__ == "__main__":
    main()