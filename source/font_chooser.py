import tkinter as tk
from tkinter import ttk, font


class FontChooser:
    """Font choosing dialog"""

    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(parent.master)
        self.top.title('Pop Out')
        self.font_name_label = None
        self.font_name_list = None
        self.font_size_label = None
        self.font_size_list = None
        self.apply_btn = None
        self.create_widgets()
        self.populate_data()

    def create_widgets(self):
        self.font_name_label = tk.Label(self.top, text='Font Name')
        self.font_name_label.grid(row=0, column=0, pady=(5, 0), padx=(1, 0))

        self.font_name_list = tk.Listbox(self.top, width=30, selectmode=tk.SINGLE, exportselection=False)
        self.font_name_list.grid(row=1, column=0, pady=(1, 5), padx=(5, 0))

        scrollbar_font_name = ttk.Scrollbar(self.top, orient="vertical")
        scrollbar_font_name.config(command=self.font_name_list.yview)
        scrollbar_font_name.grid(row=1, column=1, sticky='nsew', padx=(0, 10))
        self.font_name_list.config(yscrollcommand=scrollbar_font_name.set)

        self.font_size_label = tk.Label(self.top, text='Font Size')
        self.font_size_label.grid(row=0, column=2, pady=(5, 0), padx=(1, 0))

        self.font_size_list = tk.Listbox(self.top, width=7, selectmode=tk.SINGLE, exportselection=False)
        self.font_size_list.grid(row=1, column=2, pady=(1, 5), padx=(5, 0))

        scrollbar_font_size = ttk.Scrollbar(self.top, orient="vertical")
        scrollbar_font_size.config(command=self.font_size_list.yview)
        scrollbar_font_size.grid(row=1, column=3, sticky='nsew', padx=(0, 10))
        self.font_size_list.config(yscrollcommand=scrollbar_font_size.set)

        self.apply_btn = ttk.Button(self.top, text='Apply', command=self.apply_font_selection, style='bb.TButton')
        self.apply_btn.grid(row=2, column=2, columnspan=2, sticky='se', pady=(10, 10), padx=(0, 10))

    def populate_data(self):
        for font_family_name in font.families():
            self.font_name_list.insert(tk.END, font_family_name)

        for font_size in range(5,100):
            self.font_size_list.insert(tk.END, font_size)

    def apply_font_selection(self):
        selected_fontname = None if len(self.font_name_list.curselection()) ==0 else self.font_name_list.get(tk.ACTIVE)
        print(selected_fontname)
        self.parent.command_parser.execute('fontname={}'.format(selected_fontname))
        selected_fontsize = '0' if len(self.font_size_list.curselection()) == 0 else self.font_size_list.get(tk.ACTIVE)
        print(selected_fontsize)
        self.parent.command_parser.execute('fontsize={}'.format(selected_fontsize))
