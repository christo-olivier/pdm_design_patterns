import abc
from datetime import datetime
from typing import List

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