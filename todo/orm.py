from sqlalchemy import Table, MetaData, Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import mapper

from todo.model import ToDoItem

metadata = MetaData()

item_table = Table(
    "item",
    metadata,
    Column("name", String(250), primary_key=True, nullable=False),
    Column("due", Date, nullable=False),
    Column("completed", Date, nullable=True),
    Column("priority", String(10), nullable=True),
    Column("status", String(25), default="active", nullable=True),
)


def start_mapper():
    mapper(ToDoItem, item_table)