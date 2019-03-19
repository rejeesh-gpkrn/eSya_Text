import argparse
import os as os
import sys
import tkinter as tk
import tkinter.messagebox as tk_messagebox
from datetime import datetime
from tkinter import ttk, colorchooser
from tkinter.font import Font

import pkg_resources

from source.command_parser import CommandParser
from source.configuration import Configuration
from source.font_chooser import FontChooser
from source.note_editor import NoteEditor
from source.popout_window import PopOutWindow
from source.search_window import SearchWindow


class Application(tk.Frame):

    """Application root class"""

    APPLICATION_ROOT = None

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.global_settings()
        self.note_editor_dictionary = {}
        self.command_var = tk.StringVar()
        self.command_parser = CommandParser()
        self.command_parser.command_router.note_editor_dictionary = self.note_editor_dictionary
        self.command_parser.command_router.home_screen = self
        self.font_bold_enabled = tk.IntVar()
        self.create_widgets()
        self.key_binding()
        self.process_command_line()

    def global_settings(self):
        # Application.APPLICATION_ROOT = os.path.dirname(sys.modules['__main__'].__file__)
        print('eSya Text started from location [', Application.APPLICATION_ROOT, ']')

        s = ttk.Style()
        s.configure('bb.TButton', padding=1, width=7)

        # Menu style
        s_menu_button = ttk.Style()
        s_menu_button.configure('TMenubutton', padding=1, height=1, background='lightgray')

    def process_command_line(self):
        command_line_parser = argparse.ArgumentParser(description='Open file for read and write.')
        command_line_parser.add_argument('-f', '--file', metavar='FILE', default='', help='Full path of file to open')
        command_line_arguments = command_line_parser.parse_args()
        if command_line_arguments.file is not None and command_line_arguments.file != '':
            self.read(command_line_arguments.file)

    def key_binding(self):
        self.master.protocol('WM_DELETE_WINDOW', self.on_delete_window)
        self.master.bind("<Control-s>", self.control_s)
        self.master.bind("<Control-S>", self.control_s)
        self.master.bind("<Control-n>", self.control_n)
        self.master.bind("<Control-N>", self.control_n)
        self.master.bind("<Control-o>", self.control_o)
        self.master.bind("<Control-O>", self.control_o)
        self.master.bind("<Control-f>", self.control_f)
        self.master.bind("<Control-F>", self.control_f)

    def create_widgets(self):
        icon_image_root = os.path.join(Application.APPLICATION_ROOT, 'source', 'image')

        self.toolbar = tk.Frame(self, bg="#eee")
        self.toolbar.pack(side="top", fill="x")

        # Menu definition
        self.options_btn = ttk.Menubutton(self.toolbar, text='〓')
        self.options_btn.menu = tk.Menu(self.options_btn, tearoff=0, background='white')
        self.options_btn["menu"] = self.options_btn.menu
        format_menu = tk.Menu(self.toolbar, tearoff=False, background='white')
        format_menu.add_checkbutton(label="Emphasize", variable=self.font_bold_enabled, command=self.enable_emphasize)
        format_menu.add_command(label='Font', underline=0, command=self.choose_editor_font)
        color_menu = tk.Menu(self.toolbar, tearoff=False, background='white')
        color_menu.add_command(label='Background', underline=0, command=self.choose_editor_bgcolor)
        color_menu.add_command(label='Text Color', underline=0, command=self.choose_editor_fgcolor)
        format_menu.add_cascade(label='Color', underline=0, menu=color_menu)
        self.options_btn.menu.add_cascade(label='Format', underline=0, menu=format_menu)
        self.options_btn.menu.add_command(label='Print', underline=0,
                                          command=lambda: self.command_parser.execute('print=this'))
        self.options_btn.menu.add_command(label='Save Profile', underline=0, command=self.save_profile)
        self.options_btn.menu.add_command(label='Exit', underline=0, command=self.on_delete_window)
        self.options_btn.pack(side="left")

        new_icon_path = os.path.join(icon_image_root, 'new.gif')
        new_icon = tk.PhotoImage(file=new_icon_path)
        # new_icon = tk.PhotoImage(file="source/image/new.gif")
        self.new_btn = tk.Button(self.toolbar, image=new_icon, command=self.new)
        self.new_btn.image = new_icon
        self.new_btn.config(relief=tk.GROOVE)
        self.new_btn.bind('<Enter>', self.on_enter)
        self.new_btn.bind('<Leave>', self.on_leave)
        self.new_btn.pack(side="left")

        open_icon_path = os.path.join(icon_image_root, 'open.gif')
        open_icon = tk.PhotoImage(file=open_icon_path)
        self.read_btn = tk.Button(self.toolbar, image=open_icon, command=self.read)
        self.read_btn.image = open_icon
        self.read_btn.config(relief=tk.GROOVE)
        self.read_btn.bind('<Enter>', self.on_enter)
        self.read_btn.bind('<Leave>', self.on_leave)
        self.read_btn.pack(side="left")

        save_icon_path = os.path.join(icon_image_root, 'save.gif')
        save_icon = tk.PhotoImage(file=save_icon_path)
        self.save_btn = tk.Button(self.toolbar, image=save_icon, command=self.save)
        self.save_btn.image = save_icon
        self.save_btn.config(relief=tk.GROOVE)
        self.save_btn.bind('<Enter>', self.on_enter)
        self.save_btn.bind('<Leave>', self.on_leave)
        self.save_btn.pack(side="left")

        saveas_icon_path = os.path.join(icon_image_root, 'save_as.gif')
        save_as_icon = tk.PhotoImage(file=saveas_icon_path)
        self.save_as_btn = tk.Button(self.toolbar, image=save_as_icon, command=self.save_as)
        self.save_as_btn.image = save_as_icon
        self.save_as_btn.config(relief=tk.GROOVE)
        self.save_as_btn.bind('<Enter>', self.on_enter)
        self.save_as_btn.bind('<Leave>', self.on_leave)
        self.save_as_btn.pack(side="left")

        highlight_icon_path = os.path.join(icon_image_root, 'highlight.gif')
        highlight_icon = tk.PhotoImage(file=highlight_icon_path)
        self.highlight_btn = tk.Button(self.toolbar, image=highlight_icon, command=self.make_highlight)
        self.highlight_btn.image = highlight_icon
        self.highlight_btn.config(relief=tk.GROOVE)
        self.highlight_btn.bind('<Enter>', self.on_enter)
        self.highlight_btn.bind('<Leave>', self.on_leave)
        self.highlight_btn.pack(side="left")

        clear_icon_path = os.path.join(icon_image_root, 'clear.gif')
        clear_icon = tk.PhotoImage(file=clear_icon_path)
        self.clear_btn = tk.Button(self.toolbar, image=clear_icon, command=self.clear)
        self.clear_btn.image = clear_icon
        self.clear_btn.config(relief=tk.GROOVE)
        self.clear_btn.bind('<Enter>', self.on_enter)
        self.clear_btn.bind('<Leave>', self.on_leave)
        self.clear_btn.pack(side="left")

        search_icon_path = os.path.join(icon_image_root, 'search.gif')
        search_icon = tk.PhotoImage(file=search_icon_path)
        self.searrch_btn = tk.Button(self.toolbar, image=search_icon, command=self.search)
        self.searrch_btn.image = search_icon
        self.searrch_btn.config(relief=tk.GROOVE)
        self.searrch_btn.bind('<Enter>', self.on_enter)
        self.searrch_btn.bind('<Leave>', self.on_leave)
        self.searrch_btn.pack(side="left")

        popout_icon_path = os.path.join(icon_image_root, 'popout.gif')
        popout_icon = tk.PhotoImage(file=popout_icon_path)
        self.popout_btn = tk.Button(self.toolbar, image=popout_icon, command=self.pop_out)
        self.popout_btn.image = popout_icon
        self.popout_btn.config(relief=tk.GROOVE)
        self.popout_btn.bind('<Enter>', self.on_enter)
        self.popout_btn.bind('<Leave>', self.on_leave)
        self.popout_btn.pack(side="left")

        # Command box
        self.command_label = tk.Label(self.toolbar, text='  >')
        self.command_label.pack(side='left')

        self.command_box = tk.Entry(self.toolbar, textvariable=self.command_var)
        self.command_box.config(bg='#CCDDFF')
        self.command_box.config(fg='#771133')
        self.command_box.bind('<Return>', self.command_issue)
        self.command_box.config(relief=tk.GROOVE)
        self.command_box.pack(side='left', ipady=0.01)

        command_issue_icon_path = os.path.join(icon_image_root, 'command_issue.gif')
        command_issue_icon = tk.PhotoImage(file=command_issue_icon_path)
        self.command_issue_btn = tk.Button(self.toolbar, image=command_issue_icon, command=self.command_issue)
        self.command_issue_btn.image = command_issue_icon
        self.command_issue_btn.config(relief=tk.GROOVE)
        self.command_issue_btn.bind('<Enter>', self.on_enter)
        self.command_issue_btn.bind('<Leave>', self.on_leave)
        self.command_issue_btn.pack(side="left")

        close_icon_path = os.path.join(icon_image_root, 'close.gif')
        close_icon = tk.PhotoImage(file=close_icon_path)
        self.close_btn = tk.Button(self.toolbar, image=close_icon, command=self.close)
        self.close_btn.image = close_icon
        self.close_btn.config(relief=tk.FLAT)
        self.close_btn.bind('<Enter>', self.on_enter_close)
        self.close_btn.bind('<Leave>', self.on_leave_close)
        self.close_btn.pack(side="right")

        # Creates a bold font
        self.bold_font = Font(family="Helvetica", size=14, weight="bold")

        # Notebook definition
        self.notebook = ttk.Notebook(self, width=self.master.winfo_screenwidth())
        self.notebook.pack(fill='both', expand=True)

        # Still not persistence found
        self.new()

    def create_editor_frame(self, note_editor):
        # Editor section
        editor_frame = tk.Frame(self.notebook, width=self.master.winfo_screenwidth(), height=50)
        # editor_frame.pack(side="top")
        # editor_frame.pack(fill="both", expand=True)
        editor_frame.pack(side='top', fill='both', expand=True)
        self.notebook.add(editor_frame, text=note_editor.page_name)
        note_editor.id = self.notebook.tabs()[-1]
        self.notebook.select(note_editor.id)

        # Horizontal scrollbar
        horizontal_scrollbar = tk.Scrollbar(editor_frame, orient=tk.HORIZONTAL)
        horizontal_scrollbar.pack(side="top", fill="x")

        note_editor.create_editor(editor_frame)
        note_editor.editor['height'] = 46
        note_editor.editor['width'] = self.master.winfo_screenwidth()

        # Set target text box to horizontal scrollbar
        horizontal_scrollbar["command"] = note_editor.editor.xview
        note_editor.editor['xscrollcommand'] = horizontal_scrollbar.set

    def show_options(self):
        print('options selected')

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
            return False
        else:
            self.note_editor_dictionary[tab_id].page_name = os.path.basename(
                self.note_editor_dictionary[tab_id].file_io.file_name)
            self.notebook.tab(tab_id, text=self.note_editor_dictionary[tab_id].page_name)
            self.show_status('Saved successfully.')
            self.note_editor_dictionary[tab_id].editor.edit_modified(False)
            return True

    def save_as(self):
        tab_id = self.notebook.select()
        data_to_copy = self.note_editor_dictionary[tab_id].editor.get("1.0", 'end-1c')
        self.new()
        new_tab_id = self.notebook.select()
        self.note_editor_dictionary[new_tab_id].editor.insert(tk.END, data_to_copy)
        self.save()

    def read(self, external_file_name = None):
        note_editor = NoteEditor()
        file_read_status = note_editor.file_io.read(external_file_name)
        if file_read_status is None:
            note_editor.page_name = os.path.basename(note_editor.file_io.file_name)
            self.create_editor_frame(note_editor)
            note_editor.editor.insert(tk.END, note_editor.file_io.file_data)
            self.note_editor_dictionary[note_editor.id] = note_editor
            note_editor.editor.edit_modified(False)
            return True
        else:
            tk_messagebox.showerror('Failed', file_read_status)
            return False

    def make_highlight(self):
        # tk.TclError exception is raised if not text is selected
        try:
            tab_id = self.notebook.select()
            self.note_editor_dictionary[tab_id].editor.tag_add("HIGHLIGHT", "sel.first", "sel.last")
            self.note_editor_dictionary[tab_id].editor.tag_add("BACKGROUND", "sel.first", "sel.last")
            self.show_status('Selection highlighted.')
        except tk.TclError:
            pass

    def clear(self):
        tab_id = self.notebook.select()
        self.note_editor_dictionary[tab_id].editor.tag_remove("HIGHLIGHT", "1.0", 'end')
        self.note_editor_dictionary[tab_id].editor.tag_remove("BACKGROUND", "1.0", 'end')
        self.show_status('Highlight cleared.')

    def close(self):
        tab_id = self.notebook.select()
        is_dirty = self.note_editor_dictionary[tab_id].is_dirty()
        is_user_selection_close = False
        if is_dirty:
            dirty_window_close_message = '{} contains changes. ' \
                                         '\nDo you want to save it?'\
                                        .format(self.note_editor_dictionary[tab_id].page_name)
            is_user_selection_close = tk_messagebox.askyesnocancel('Close', dirty_window_close_message)
        if is_user_selection_close is None:
            return False
        elif not is_dirty or not is_user_selection_close:
            self.notebook.forget(tab_id)
            del self.note_editor_dictionary[tab_id]
            return True
        else:
            save_status = self.save()
            return save_status

    def search(self):
        search_option_window = SearchWindow(self)
        search_option_window.top.wm_attributes("-topmost", 1)
        tab_id = self.notebook.select()
        self.note_editor_dictionary[tab_id].editor.mark_set(tk.INSERT, '1.0')
        self.master.wait_window(search_option_window.top)

    def search_forward(self, text):
        tab_id = self.notebook.select()
        found_search_element = self.note_editor_dictionary[tab_id].search_forward(text)
        if not found_search_element:
            tk_messagebox.showinfo('Search', '{} not found.'.format(text))

    def search_backward(self, text):
        tab_id = self.notebook.select()
        found_search_element = self.note_editor_dictionary[tab_id].search_backward(text)
        if not found_search_element:
            tk_messagebox.showinfo('Search', '{} not found.'.format(text))

    def replace_selected_text(self, new_text):
        tab_id = self.notebook.select()
        self.note_editor_dictionary[tab_id].replace_selected_text(new_text)

    def pop_out(self):
        pop_out_window = PopOutWindow(self)
        pop_out_window.top.wm_attributes("-topmost", 1)
        self.master.wait_window(pop_out_window.top)
        self.show_status('Pop out closed.')

    def selected_data(self):
        tab_id = self.notebook.select()
        if self.note_editor_dictionary[tab_id].editor.tag_ranges(tk.SEL):
            selected_text = self.note_editor_dictionary[tab_id].editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            return selected_text
        return None

    def dock_popup(self, data):
        self.new()
        new_tab_id = self.notebook.select()
        self.note_editor_dictionary[new_tab_id].editor.insert(tk.END, data)
        doc_page_name = 'DOCK|{}'.format(datetime.now())
        self.notebook.tab(new_tab_id, text=doc_page_name)

    def choose_editor_bgcolor(self):
        (triple, hexstr) = colorchooser.askcolor()
        if hexstr:
            tab_id = self.notebook.select()
            self.note_editor_dictionary[tab_id].set_editor_bgcolor(hexstr)

    def choose_editor_fgcolor(self):
        (triple, hexstr) = colorchooser.askcolor()
        if hexstr:
            tab_id = self.notebook.select()
            self.note_editor_dictionary[tab_id].set_editor_fgcolor(hexstr)

    def choose_editor_font(self):
        font_chooser_window = FontChooser(self)
        font_chooser_window.top.wm_attributes("-topmost", 1)
        self.master.wait_window(font_chooser_window.top)

    def enable_emphasize(self):
        tab_id = self.notebook.select()
        self.note_editor_dictionary[tab_id].set_emphasis(self.font_bold_enabled.get())

    def print_document(self, file_name):
        os.startfile(file_name, 'print')

    def command_issue(self, event=None):
        tab_id = self.notebook.select()
        result = self.command_parser.execute(self.command_var.get())
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

    def control_n(self, event):
        print(repr(event.char), 'New key combination.')
        self.new()

    def control_o(self, event):
        print(repr(event.char), 'Open key combination.')
        self.read()

    def control_f(self, event):
        print(repr(event.char), 'Search key combination.')
        self.search()

    def on_delete_window(self):
        present_tab_count = len(self.notebook.tabs())
        while present_tab_count > 0:
            close_status = self.close()
            if not close_status:
                return
            else:
                present_tab_count -= 1

        self.master.destroy()
        print('eSya Text exited.')

    def save_profile(self):
        pass

    # TODO: Move to it's own class
    def show_status(self, message):
        toplevel = tk.Toplevel(self.master, width=200, height=60)
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
