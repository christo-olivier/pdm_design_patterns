import abc
import csv
from datetime import datetime
from typing import Dict, List

from sqlalchemy.exc import IntegrityError

from todo.model import ToDoItem


class NoItemFoundError(Exception):
    """
    Exception to raise when no item is found in the repository.
    """


class ItemAlreadyExistsError(Exception):
    """
    Exception raised when the same item already exists in the database and
    the user is trying to insert it again.
    """


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item: ToDoItem):
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[ToDoItem]:
        raise NotImplementedError

    @abc.abstractmethod
    def mark_complete(self, name: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_item(self, name: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update_item(self, name: str, due: str, priority: str) -> None:
        raise NotImplementedError


class SQLRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, item: ToDoItem) -> None:
        """
        Add a todo item to the database.
        """
        try:
            self.session.add(item)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise ItemAlreadyExistsError(f"Item `{item.name}` already exists.")

    def list(self) -> None:
        """
        Return all of the items in the database.
        """
        return self.session.query(ToDoItem).all()

    def mark_complete(self, name: str) -> None:
        """
        Mark a todo item as completed.
        """
        item = self.session.query(ToDoItem).filter(ToDoItem.name == name).first()

        if not item:
            raise NoItemFoundError("No todo item with name `{name}` found.")

        item.status = "complete"
        item.completed = datetime.now().date()
        self.session.commit()

    def remove_item(self, name: str) -> None:
        """
        Remove a todo item from the database.
        """
        item = self.session.query(ToDoItem).filter(ToDoItem.name == name).first()

        if not item:
            raise NoItemFoundError(f"No todo item with name `{name}` found.")

        self.session.delete(item)
        self.session.commit()

    def update_item(self, name: str, due: str, priority: str) -> None:
        """
        Update an item's properties.
        """
        try:
            item = self.session.query(ToDoItem).filter_by(name=name).first()
            item.due = self._convert_to_date(due)
            item.priority = priority
            item.completed = None
            self.session.commit()
        except AttributeError:
            raise NoItemFoundError(f"No todo item with name `{name}` found.")

    @staticmethod
    def _convert_to_date(date_str: str) -> datetime.date:
        """
        Convert a date string to a date object.
        """
        return datetime.strptime(date_str, "%Y-%m-%d").date()


class CSVRepository(AbstractRepository):
    def __init__(self, db_path):
        self.db_path = db_path
        self.items: dict = self._load_from_db()

    def add(self, item: ToDoItem) -> None:
        """
        Add a todo item to the database.
        """
        if item.name in self.items:
            raise ItemAlreadyExistsError(f"Item `{item.name}` already exists.")

        self.items[item.name] = item
        self._save_to_db()

    def list(self) -> None:
        """
        Return all of the items in the database.
        """
        return self.items.values()

    def mark_complete(self, name: str) -> None:
        """
        Mark a todo item as completed.
        """
        try:
            item = self.items[name]

            item.status = "complete"
            item.completed = datetime.now().date()
            self.items[name] = item
            self._save_to_db()
        except KeyError:
            raise NoItemFoundError("No todo item with name `{name}` found.")

    def remove_item(self, name: str) -> None:
        """
        Remove a todo item from the database.
        """
        if name not in self.items:
            raise NoItemFoundError(f"No todo item with name `{name}` found.")

        del self.items[name]
        self._save_to_db()

    def update_item(self, name: str, due: str, priority: str) -> None:
        """
        Update an item's properties.
        """
        if name not in self.items:
            raise NoItemFoundError(f"No todo item with name `{name}` found.")

        item = self.items[name]
        item.due = self._convert_to_date(due)
        item.priority = priority
        item.status = "active"
        item.completed = None
        self.items[name] = item
        self._save_to_db()

    @staticmethod
    def _convert_to_date(date_str: str) -> datetime.date:
        """
        Convert a date string to a date object.
        """
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    def _load_from_db(self) -> Dict[str, ToDoItem]:
        """
        Load the database file from disk and retrieve all of the ToDoItems in it.
        """
        # Open file with append + to create and read if it does not exist
        # a+ seeks to the end of the file so set seek to start of file before
        # reading.
        with open(self.db_path, "a+", newline="") as csv_file:
            csv_file.seek(0)

            reader = csv.DictReader(csv_file)
            return {
                row.get("name"): ToDoItem(
                    name=row.get("name"),
                    due=self._convert_to_date(row.get("due")),
                    priority=row.get("priority"),
                    completed=row.get("completed"),
                    status=row.get("status"),
                )
                for row in reader
            }

    def _save_to_db(self) -> None:
        """
        Save the items to the database file on disk.
        """
        with open(self.db_path, "w", newline="") as csv_file:
            fieldnames = ToDoItem.__dataclass_fields__.keys()
            writer = csv.DictWriter(csv_file, fieldnames)

            writer.writeheader()
            for item in self.items.values():
                writer.writerow(item.__dict__)