import os as os
import sys as sys
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font
from datetime import datetime
import tkinter.messagebox as tk_messagebox

from source.command_parser import CommandParser
from source.configuration import Configuration
from source.file_io import FileIO
from source.note_editor import NoteEditor


class Application(tk.Frame):

    """Application root class"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.note_editor_dictionary = {}
        self.command_var = tk.StringVar()
        self.command_parser = CommandParser()
        self.create_widgets()
        self.key_binding()

    def key_binding(self):
        self.master.bind("<Control-s>", self.control_s)
        self.master.bind("<Control-S>", self.control_s)

    def create_widgets(self):
        self.toolbar = tk.Frame(self, bg="#eee")
        self.toolbar.pack(side="top", fill="x")

        new_icon = tk.PhotoImage(file="source/image/new.gif")
        self.new_btn = tk.Button(self.toolbar, image=new_icon, command=self.new)
        self.new_btn.image = new_icon
        self.new_btn.config(relief=tk.GROOVE)
        self.new_btn.bind('<Enter>', self.on_enter)
        self.new_btn.bind('<Leave>', self.on_leave)
        self.new_btn.pack(side="left")

        open_icon = tk.PhotoImage(file="source/image/open.gif")
        self.read_btn = tk.Button(self.toolbar, image=open_icon, command=self.read)
        self.read_btn.image = open_icon
        self.read_btn.config(relief=tk.GROOVE)
        self.read_btn.bind('<Enter>', self.on_enter)
        self.read_btn.bind('<Leave>', self.on_leave)
        self.read_btn.pack(side="left")

        save_icon = tk.PhotoImage(file="source/image/save.gif")
        self.save_btn = tk.Button(self.toolbar, image=save_icon, command=self.save)
        self.save_btn.image = save_icon
        self.save_btn.config(relief=tk.GROOVE)
        self.save_btn.bind('<Enter>', self.on_enter)
        self.save_btn.bind('<Leave>', self.on_leave)
        self.save_btn.pack(side="left")

        save_as_icon = tk.PhotoImage(file="source/image/save_as.gif")
        self.save_as_btn = tk.Button(self.toolbar, image=save_as_icon, command=self.save_as)
        self.save_as_btn.image = save_as_icon
        self.save_as_btn.config(relief=tk.GROOVE)
        self.save_as_btn.bind('<Enter>', self.on_enter)
        self.save_as_btn.bind('<Leave>', self.on_leave)
        self.save_as_btn.pack(side="left")

        highlight_icon = tk.PhotoImage(file="source/image/highlight.gif")
        self.highlight_btn = tk.Button(self.toolbar, image=highlight_icon, command=self.make_highlight)
        self.highlight_btn.image = highlight_icon
        self.highlight_btn.config(relief=tk.GROOVE)
        self.highlight_btn.bind('<Enter>', self.on_enter)
        self.highlight_btn.bind('<Leave>', self.on_leave)
        self.highlight_btn.pack(side="left")

        clear_icon = tk.PhotoImage(file="source/image/clear.gif")
        self.clear_btn = tk.Button(self.toolbar, image=clear_icon, command=self.clear)
        self.clear_btn.image = clear_icon
        self.clear_btn.config(relief=tk.GROOVE)
        self.clear_btn.bind('<Enter>', self.on_enter)
        self.clear_btn.bind('<Leave>', self.on_leave)
        self.clear_btn.pack(side="left")

        # Command box
        self.command_label = tk.Label(self.toolbar, text='  >')
        self.command_label.pack(side='left')

        self.command_box = tk.Entry(self.toolbar, textvariable=self.command_var)
        self.command_box.config(bg='#CCDDFF')
        self.command_box.config(fg='#771133')
        self.command_box.bind('<Return>', self.command_issue)
        self.command_box.config(relief=tk.GROOVE)
        self.command_box.pack(side='left')

        command_issue_icon = tk.PhotoImage(file="source/image/command_issue.gif")
        self.command_issue_btn = tk.Button(self.toolbar, image=command_issue_icon, command=self.command_issue)
        self.command_issue_btn.image = command_issue_icon
        self.command_issue_btn.config(relief=tk.GROOVE)
        self.command_issue_btn.bind('<Enter>', self.on_enter)
        self.command_issue_btn.bind('<Leave>', self.on_leave)
        self.command_issue_btn.pack(side="left")


        close_icon = tk.PhotoImage(file="source/image/close.gif")
        self.close = tk.Button(self.toolbar, image=close_icon, command=self.close)
        self.close.image = close_icon
        self.close.config(relief=tk.FLAT)
        self.close.bind('<Enter>', self.on_enter_close)
        self.close.bind('<Leave>', self.on_leave_close)
        self.close.pack(side="right")

        # Creates a bold font
        self.bold_font = Font(family="Helvetica", size=14, weight="bold")

        # Notebook definition
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        # Still not persistence found
        self.new()

    def create_editor_frame(self, note_editor):
        # Editor section
        editor_frame = tk.Frame(self.notebook, width=self.master.winfo_screenwidth(), height=50)
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
        file_write_status = self.note_editor_dictionary[tab_id].file_io.save()
        if file_write_status is not None:
            tk_messagebox.showerror('Failed', file_write_status)
        else:
            self.note_editor_dictionary[tab_id].page_name = os.path.basename(
                self.note_editor_dictionary[tab_id].file_io.file_name)
            self.notebook.tab(tab_id, text=self.note_editor_dictionary[tab_id].page_name)
            self.show_status('Saved successfully.')

    def save_as(self):
        tab_id = self.notebook.select()
        data_to_copy = self.note_editor_dictionary[tab_id].editor.get("1.0", 'end-1c')
        self.new()
        new_tab_id = self.notebook.select()
        self.note_editor_dictionary[new_tab_id].editor.insert(tk.END, data_to_copy)
        self.save()

    def read(self):
        note_editor = NoteEditor()
        file_read_status = note_editor.file_io.read()
        if file_read_status is None:
            note_editor.page_name = os.path.basename(note_editor.file_io.file_name)
            self.create_editor_frame(note_editor)
            note_editor.editor.insert(tk.END, note_editor.file_io.file_data)
            self.note_editor_dictionary[note_editor.id] = note_editor
        else:
            tk_messagebox.showerror('Failed', file_read_status)

    def make_highlight(self):
        # tk.TclError exception is raised if not text is selected
        try:
            tab_id = self.notebook.select()
            self.note_editor_dictionary[tab_id].editor.tag_add("BOLDFONT", "sel.first", "sel.last")
            self.note_editor_dictionary[tab_id].editor.tag_add("HIGHLIGHT", "sel.first", "sel.last")
            self.note_editor_dictionary[tab_id].editor.tag_add("BACKGROUND", "sel.first", "sel.last")
            self.show_status('Selection highlighted.')
        except tk.TclError:
            pass

    def clear(self):
        tab_id = self.notebook.select()
        self.note_editor_dictionary[tab_id].editor.tag_remove("BOLDFONT", "1.0", 'end')
        self.note_editor_dictionary[tab_id].editor.tag_remove("HIGHLIGHT", "1.0", 'end')
        self.note_editor_dictionary[tab_id].editor.tag_remove("BACKGROUND", "1.0", 'end')
        self.show_status('Highlight cleared.')

    def close(self):
        tab_id = self.notebook.select()
        self.notebook.forget(tab_id)
        del self.note_editor_dictionary[tab_id]

    def command_issue(self, event=None):
        tab_id = self.notebook.select()
        result = self.command_parser.execute(self.command_var.get())
        # result = Configuration.execute_user_command(self.command_var.get())
        error_message = None
        if result == 1:
            error_message = 'No command specified'
        elif result == 2:
            error_message = 'Expected command format is "key:value"'
        elif result == 3:
            error_message = 'Can\'t perform the action'
        else:
            error_message = None

        if result != 0:
            tk_messagebox.showerror('Failed', error_message)
        else:
            print('Updated user commands [', Configuration.common, ']')
            self.show_status('Executed successfully.')

    def on_enter(self, e):
        e.widget.config(relief=tk.RIDGE)

    def on_leave(self, e):
        e.widget.config(relief=tk.GROOVE)

    def on_enter_close(self, e):
        e.widget.config(relief=tk.RIDGE)

    def on_leave_close(self, e):
        e.widget.config(relief=tk.FLAT)

    def control_s(self, event):
        print(repr(event.char), 'Save key combination.')
        self.save()

    def show_status(self, message):
        toplevel = tk.Toplevel(self.master, width=150, height=60)
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        w = toplevel.winfo_reqwidth()
        h = toplevel.winfo_reqheight()
        x = (width // 2) - (w // 2)
        y = (height // 2) - (h // 2)
        toplevel.geometry('{}x{}+{}+{}'.format(w, h, x, y))
        label1 = tk.Label(toplevel, text=message, height=60, width=150, borderwidth=2, relief="groove", fg="#535353")
        label1.pack()
        toplevel.overrideredirect(True)
        toplevel.after(1000, lambda: toplevel.destroy())
