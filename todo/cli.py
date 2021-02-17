import sys


def main(args=None):
    if not args:
        args = sys.argv[1:]

    command = args[0].lower()

    if command == "add":
        pass

    if command == "update":
        pass

    if command == "remove":
        pass

    if command == "due":
        pass


if __name__ == "__main__":
    main(sys.argv[1:])