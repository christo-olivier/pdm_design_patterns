import pathlib

db_path = pathlib.Path(__file__).resolve().parent.joinpath("data")
print(db_path)