from source.configuration import Configuration


class CommandRouter:
    def __init__(self):
        self.note_editor_dictionary = None
        self.home_screen = None
        print('Command Router initiated')

    def encoding(self, value):
        Configuration.common['encoding'] = value

    def fontname(self, value):
        Configuration.common['fontname'] = value
        tab_id = self.home_screen.notebook.select()
        self.note_editor_dictionary[tab_id].set_editor_font(value, None)

    def fontsize(self, value):
        Configuration.common['fontsize'] = value
        tab_id = self.home_screen.notebook.select()
        self.note_editor_dictionary[tab_id].set_editor_font(None, value)

    def remove(self, value):
        if value in Configuration.common:
            del(Configuration.common[value])
