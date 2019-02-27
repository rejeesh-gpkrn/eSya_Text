from source.configuration import Configuration


class CommandRouter:
    def __init__(self):
        print('Command Router initiated')

    def encoding(self, value):
        Configuration.common['encoding'] = value

    def remove(self, value):
        if value in Configuration.common:
            del(Configuration.common['encoding'])
