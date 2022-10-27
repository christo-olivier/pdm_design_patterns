from dataclasses import dataclass

from datetime import date


@dataclass()
class ToDoItem:
    name: str
    due: date
    priority: str
    completed: date = None
    status: str = None
