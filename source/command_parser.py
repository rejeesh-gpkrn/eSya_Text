from source.command_router import CommandRouter


class CommandParser:

    def __init__(self):
        self.command_router = CommandRouter()

    def execute(self, command):
        # Parse the command using parser
        # Assign to corresponding person
        if command is None or command == '':
            return 1

        tokens = command.split('=')
        if len(tokens) < 2:
            return 2

        key = tokens[0].strip().lower()
        value = tokens[1].strip()
        if not hasattr(self.command_router, key):
            return 3

        getattr(self.command_router, key)(value)

        return 0
