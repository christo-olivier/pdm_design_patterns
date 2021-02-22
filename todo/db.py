from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todo.orm import metadata, start_mapper

# Setup database and session object
db_path = "/Users/christo/repos/todo/todo_app.sqlite"
engine = create_engine(f"sqlite:///{db_path}")
metadata.create_all(engine)
start_mapper()
get_session = sessionmaker(bind=engine)
session = get_session()