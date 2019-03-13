import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class PopOutWindow:
    """Pop out window which is used to snap multiple tab contents"""

    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(parent.master)
        self.top.title('Pop Out')
        self.editor = None
        self.toolbar = None
        self.create_widgets()

    def create_widgets(self):
        self.toolbar = tk.Frame(self.top, bg="#eee")
        self.toolbar.pack(side="top", fill="x")

        self.catch_btn = ttk.Button(self.toolbar, text='Catch', command=self.catch_data, style='bb.TButton')
        self.catch_btn.pack(side="left", pady=(2, 2), padx=(2, 1))

        self.dock_btn = ttk.Button(self.toolbar, text='Dock', command=self.dock_window, style='bb.TButton')
        self.dock_btn.pack(side="left", pady=(2, 2), padx=(1, 2))

        # Horizontal scrollbar
        horizontal_scrollbar = tk.Scrollbar(self.top, orient=tk.HORIZONTAL)
        horizontal_scrollbar.pack(side="top", fill="x")

        self.editor = ScrolledText(self.top, width=60, height=20)
        self.editor.pack(fill="both", expand=True)
        self.editor['wrap'] = tk.NONE
        self.editor['background'] = '#FEFCD7'
        self.editor['foreground'] = 'blue'

        # Set target text box to horizontal scrollbar
        horizontal_scrollbar["command"] = self.editor.xview
        self.editor['xscrollcommand'] = horizontal_scrollbar.set

    def catch_data(self):
        caught_data = self.parent.selected_data()
        if caught_data is not None:
            self.editor.insert(tk.END, caught_data)

    def dock_window(self):
        dockable_data = self.editor.get("1.0", 'end-1c')
        if dockable_data is not None and dockable_data != '':
            self.parent.dock_popup(dockable_data)

        self.top.destroy()
