import sys
from datetime import datetime

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
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def _print_item(item: Item):
    print(f"Name: {item.name}, Due: {item.due}, Priority: {item.priority}")


def _get_args():
    if len(sys.argv) < 2:
        print("Please specify your command.")
        sys.exit(1)

    args = sys.argv[1:]

    return args


def add_item(name: str, due: str, priority: str) -> None:
    try:
        new_todo = Item(name=name, due=_convert_to_date(due), priority=priority.lower())
        session.add(new_todo)
        session.commit()
    except IntegrityError:
        print("Todo item already exists.")
        session.rollback()


def remove_item(name: str) -> None:
    item = session.query(Item).filter(Item.name == name).first()

    if not item:
        print(f"No todo item with name `{name}` found.")
        return

    session.delete(item)
    session.commit()


def update_item(name: str, due: str, priority: str) -> None:
    try:
        item = session.query(Item).filter_by(name=name).first()
        item.due = _convert_to_date(due)
        item.priority = priority
        session.commit()
    except AttributeError:
        print(f"No todo item with name `{name}` found.")


def show_all() -> None:
    items = session.query(Item).all()
    for item in items:
        _print_item(item)


def show_due(due: str) -> None:
    if due.lower() == "today":
        due = datetime.now().date()
    else:
        due = _convert_to_date(due)

    items = session.query(Item).filter(Item.due <= due)
    for item in items:
        _print_item(item)


def main():
    args = _get_args()

    command = args[0].lower()

    if command == "add":
        add_item(args[1], args[2], args[3])

    if command == "update":
        update_item(args[1], args[2], args[3])

    if command == "remove":
        remove_item(args[1])

    if command == "due":
        show_due(args[1])

    if command == "all":
        show_all()


if __name__ == "__main__":
    main()