import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font
from source.file_io import FileIO


class NoteEditor:
    def __init__(self):
        self.id = None
        self.page_name = None
        # Creates a bold font
        self.bold_font = Font(family="Helvetica", size=14, weight="bold")
        self.editor = None
        self.file_io = FileIO()

    def create_editor(self, master):
        self.editor = ScrolledText(master)
        self.editor.pack(side="left")
        self.editor.focus()
        self.editor.pack(fill="both", expand=True)

        # Configuring style tags
        self.editor.tag_configure("BOLDFONT", font=self.bold_font)
        self.editor.tag_config("BACKGROUND", background="yellow")
        self.editor.tag_configure("HIGHLIGHT", foreground="red")
        self.editor['wrap'] = tk.NONE
