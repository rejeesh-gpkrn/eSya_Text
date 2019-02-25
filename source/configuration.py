class Configuration:
    common = {}

    def execute_user_command(command):
        # Parse the command using parser
        # Assign to corresponding person
        if command is None or command == '':
            return 1

        command = command.lower()

        tokens = command.split('=')
        if len(tokens) < 2:
            return 2

        Configuration.common[tokens[0].strip()] = tokens[1].strip()
        return 0
