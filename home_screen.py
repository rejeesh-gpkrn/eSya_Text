import os as os
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font
from datetime import datetime
from source.file_io import FileIO
from source.note_editor import NoteEditor


class Application(tk.Frame):

    """Application root class"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.note_editor_dictionary = {}
        self.create_widgets()

    def create_widgets(self):
        self.toolbar = tk.Frame(self, bg="#eee")
        self.toolbar.pack(side="top", fill="x")

        self.new_btn = tk.Button(self.toolbar, text="New", command=self.new)
        self.new_btn.pack(side="left")

        self.read_btn = tk.Button(self.toolbar, text="Open", command=self.read)
        self.read_btn.pack(side="left")

        self.save_btn = tk.Button(self.toolbar, text="Save", command=self.save)
        self.save_btn.pack(side="left")

        self.bold_btn = tk.Button(self.toolbar, text="Highlight", command=self.make_highlight)
        self.bold_btn.pack(side="left")

        self.clear_btn = tk.Button(self.toolbar, text="Clear", command=self.clear)
        self.clear_btn.pack(side="left")

        self.quit = tk.Button(self.toolbar, text="Quit", fg="red", command=self.master.destroy)
        self.quit.pack(side="right")

        # Creates a bold font
        self.bold_font = Font(family="Helvetica", size=14, weight="bold")

        # Notebook definition
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        # Still not persistence found
        self.new()

    def create_editor_frame(self, note_editor):
        # Editor section
        editor_frame = tk.Frame(self.notebook, width=root.winfo_screenwidth(), height=50)
        editor_frame.pack(side="top")
        editor_frame.pack(fill="both", expand=True)
        self.notebook.add(editor_frame, text=note_editor.page_name)
        note_editor.id = self.notebook.tabs()[-1]
        self.notebook.select(note_editor.id)

        # Horizontal scrollbar
        horizontal_scrollbar = tk.Scrollbar(editor_frame, orient=tk.HORIZONTAL)
        horizontal_scrollbar.pack(side="top", fill="x")

        note_editor.create_editor(editor_frame)
        note_editor.editor['height'] = 46
        note_editor.editor['width'] = 180

        # Set target text box to horizontal scrollbar
        horizontal_scrollbar["command"] = note_editor.editor.xview
        note_editor.editor['xscrollcommand'] = horizontal_scrollbar.set

    def new(self):
        note_editor = NoteEditor()
        note_editor.page_name = str(datetime.now())
        self.create_editor_frame(note_editor)
        self.note_editor_dictionary[note_editor.id] = note_editor

    def save(self):
        tab_id = self.notebook.select()
        self.note_editor_dictionary[tab_id].file_io.file_data = self.note_editor_dictionary[tab_id].editor.get("1.0", 'end-1c')
        self.note_editor_dictionary[tab_id].file_io.save()

    def read(self):
        note_editor = NoteEditor()
        is_file_read_success = note_editor.file_io.read()
        if is_file_read_success:
            note_editor.page_name = os.path.basename(note_editor.file_io.file_name)
            self.create_editor_frame(note_editor)
            note_editor.editor.insert(tk.END, note_editor.file_io.file_data)
            self.note_editor_dictionary[note_editor.id] = note_editor

    def make_highlight(self):
        # tk.TclError exception is raised if not text is selected
        try:
            self.note_editor.editor.tag_add("BOLDFONT", "sel.first", "sel.last")
            self.note_editor.editor.tag_add("HIGHLIGHT", "sel.first", "sel.last")
            self.note_editor.editor.tag_add("BACKGROUND", "sel.first", "sel.last")
        except tk.TclError:
            pass

    def clear(self):
        self.note_editor.editor.tag_remove("BOLDFONT", "1.0", 'end')
        self.note_editor.editor.tag_remove("HIGHLIGHT", "1.0", 'end')
        self.note_editor.editor.tag_remove("BACKGROUND", "1.0", 'end')


if __name__ == '__main__':
    root = tk.Tk()
    root.state('zoomed')
    root.title('eSya Text')
    # root.tk.call('tk', 'scaling', 1.0)
    app = Application(master=root)
    app.mainloop()
