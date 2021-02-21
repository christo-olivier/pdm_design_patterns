import sys

from todo import data


def _get_args():
    """
    Get the arguments passed to the application from the command line.
    """
    if len(sys.argv) < 2:
        print("Please specify your command.")
        sys.exit(1)

    args = sys.argv[1:]

    return args


def main():
    """
    Main application loop.
    """
    args = _get_args()

    # Get the command from the commandline arguments.
    command = args[0].lower()

    # Execute commands
    if command == "add":
        data.add_item(args[1], args[2], args[3])

    if command == "all":
        data.show_all()

    if command == "complete":
        data.mark_complete(args[1])

    if command == "due":
        data.show_due(args[1])

    if command == "remove":
        data.remove_item(args[1])

    if command == "update":
        data.update_item(args[1], args[2], args[3])


if __name__ == "__main__":
    main()