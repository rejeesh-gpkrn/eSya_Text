from source.configuration import Configuration
from source.sftp_file_io import SFTPFileIO


class CommandRouter:
    def __init__(self):
        self.note_editor_dictionary = None
        self.home_screen = None
        self.sftp_file_io = SFTPFileIO()
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

    def fontweight(self, value):
        Configuration.common['fontweight'] = value
        tab_id = self.home_screen.notebook.select()
        self.note_editor_dictionary[tab_id].set_editor_font(None, None, value)

    def print(self, value):
        print_document_name = None
        if value == 'this':
            tab_id = self.home_screen.notebook.select()
            print_document_name = self.note_editor_dictionary[tab_id].file_io.file_name
        else:
            print_document_name = value

        self.home_screen.print_document(print_document_name)

    def sftp(self, value):
        self.sftp_file_io.execute(value)
        print(value)
        # self.home_screen.sftp_read_callback()

    def syntax(self, value):
        tab_id = self.home_screen.notebook.select()
        self.note_editor_dictionary[tab_id].highlight_syntax()

    def remove(self, value):
        if value in Configuration.common:
            del(Configuration.common[value])

    # tk_chooseColor
    # from tkinter import colorchooser
    # colorchooser.askcolor(initialcolor='#ff0000')