from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    due = Column(Date, nullable=False)
    completed = Column(Date, nullable=True)
    priority = Column(String(10), nullable=True)
    status = Column(String(25), default="active", nullable=True)
