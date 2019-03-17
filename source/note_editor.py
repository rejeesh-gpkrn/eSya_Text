import tkinter as tk
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText

from source.configuration import Configuration
from source.file_io import FileIO


class NoteEditor:
    def __init__(self):
        self.id = None
        self.page_name = None
        self.font_name = 'arial'
        self.font_size = 12
        self.font_weight = tk.NORMAL
        self.editor = None
        self.file_io = FileIO()

    def create_editor(self, master):
        self.editor = ScrolledText(master, undo=True, autoseparators=True, maxundo=-1)

        # Styling of text area
        self.set_editor_font(None, None)

        self.editor.pack(side="left")
        self.editor.focus()
        self.editor.pack(fill="both", expand=True)

        # Configuring style tags
        self.editor.tag_config("BACKGROUND", background="yellow")
        self.editor.tag_configure("HIGHLIGHT", foreground="red")
        self.editor['wrap'] = tk.NONE

    def set_editor_font(self, font_name, font_size, font_weight=None):
        if font_name is not None:
            self.font_name = font_name

        if font_size is not None and int(font_size) > 0:
            self.font_size = font_size

        if font_weight is not None:
            self.font_weight = font_weight

        self.editor['font'] = Font(family=self.font_name, size=self.font_size, weight=self.font_weight)

    def set_editor_bgcolor(self, hex_color):
        self.editor['background'] = hex_color

    def set_emphasis(self, on):
        if on == 1:
            bold_font = Font(family=self.font_name, size=self.font_size, weight="bold")
            self.editor.tag_configure("BOLDFONT", font=bold_font)
            if self.editor.tag_ranges(tk.SEL):
                self.editor.tag_add("BOLDFONT", tk.SEL_FIRST, tk.SEL_LAST)
            else:
                self.editor.tag_add("BOLDFONT", "1.0", tk.END)
        else:
            self.editor.tag_remove("BOLDFONT", "1.0", tk.END)

    def search_forward(self, text):
        located_start = self.editor.search(text, tk.INSERT, stopindex=tk.END, forwards=True, nocase=True)
        located_end = '{}+{}c'.format(located_start, len(text))
        if located_start is '' or located_end is '':
            return False

        self.select_editor_location(located_start, located_end)

        # Start position is moved after current found location.
        self.editor.mark_set(tk.INSERT, located_end)
        return True

    def search_backward(self, text):
        located_start = self.editor.search(text, tk.INSERT, stopindex='1.0', backwards=True, nocase=True)
        located_end = '{}+{}c'.format(located_start, len(text))
        if located_start is '' or located_end is '':
            return False

        self.select_editor_location(located_start, located_end)

        # Start position is moved after current found location.
        self.editor.mark_set(tk.INSERT, located_start)
        return True

    def replace_selected_text(self, new_text):
        self.editor.delete('sel.first', 'sel.last')
        self.editor.insert('insert', new_text)

    def select_editor_location(self, selection_start, selection_end):
        print('Found location start: ', selection_start)
        print('Found location end: ', selection_end)
        selection_start_float = float(selection_start)
        self.editor.tag_remove(tk.SEL, "1.0", 'end')
        self.editor.tag_add(tk.SEL, selection_start, selection_end)
        self.editor.focus_force()
        self.editor.see(selection_start_float)

    def is_dirty(self):
        return self.editor.edit_modified()
