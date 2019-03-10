import tkinter as tk


class SearchWindow:
    """Search dialog for entering user options"""

    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(parent.master)
        self.top.title('Search')
        self.top.resizable(False, False)
        self.container_frame = None
        self.search_label = None
        self.search_text = None
        self.container_frame_btn = None
        self.search_next_btn = None
        self.search_back_btn = None
        self.replace_container_frame = None
        self.new_text_label = None
        self.replace_text = None
        self.switch_on_replace = None
        self.search_text_var = tk.StringVar()
        self.replace_text_var = tk.StringVar()
        self.switch_on_replace_var = tk.IntVar()
        self.create_widgets()

    def create_widgets(self):
        self.container_frame = tk.LabelFrame(self.top, text='Search options', width=50)
        self.container_frame.pack(side="top", pady=(0, 3), padx=(3, 0))
        # self.container_frame.pack(fill="y", expand=True)

        self.search_label = tk.Label(self.container_frame, text='Text')
        self.search_label.grid(row=0, column=0, pady=(10, 10), padx=(5, 5))

        self.search_text = tk.Entry(self.container_frame, width=40, textvariable=self.search_text_var)
        self.search_text.grid(row=0, column=1, pady=(10, 10), padx=(5, 5))
        self.search_text.focus()

        # self.container_frame_btn = tk.LabelFrame(self.container_frame, width=12, height=25)
        # self.container_frame_btn.pack(side='left', pady=(3, 3), padx=(3, 3))
        # self.container_frame_btn.grid(row=0, column=0, pady=(3, 3), padx=(3, 3))

        search_forward__icon = tk.PhotoImage(file="source/image/search_forward.gif")
        self.search_next_btn = tk.Button(self.container_frame, image=search_forward__icon,
                                         command=self.search_forward)
        self.search_next_btn.image = search_forward__icon
        self.search_next_btn.grid(row=0, column=2, padx=(5, 5))

        search_backward__icon = tk.PhotoImage(file="source/image/search_backward.gif")
        self.search_back_btn = tk.Button(self.container_frame, image=search_backward__icon,
                                         command=self.search_backward)
        self.search_back_btn.image = search_backward__icon
        self.search_back_btn.grid(row=0, column=3, padx=(5, 10))

        # Replace area
        self.replace_container_frame = tk.LabelFrame(self.container_frame, text='Replace options', width=50)
        self.replace_container_frame.grid(row=1, column=0, columnspan=4)
        # self.replace_container_frame = tk.LabelFrame(self.top, text='Replace options', width=50)
        # self.replace_container_frame.pack(side="top", pady=(0, 3), padx=(3, 0))
        # self.replace_container_frame.pack(fill="x", expand=True)

        self.new_text_label = tk.Label(self.replace_container_frame, text='New Text')
        self.new_text_label.grid(row=0, column=0, pady=(10, 10), padx=(5, 5))

        self.replace_text = tk.Entry(self.replace_container_frame, width=40, textvariable=self.replace_text_var)
        self.replace_text.grid(row=0, column=1, pady=(10, 10), padx=(5, 5))
        # self.replace_text.focus()

        self.switch_on_replace = tk.Button(self.replace_container_frame,
                                                width=2, height=1, justify='center',
                                                command=self.apply_style_switch_on_replace, fg='yellow')
        self.switch_on_replace.config(relief=tk.RAISED)
        self.switch_on_replace.config(text='Off')
        self.switch_on_replace.config(bg='gray')
        self.switch_on_replace.grid(row=0, column=2, pady=(10, 10), padx=(5, 10))

    def apply_style_switch_on_replace(self):
        if self.switch_on_replace_var.get() == 0:
            self.switch_on_replace_var.set(1)
            self.switch_on_replace.config(text='On')
            self.switch_on_replace.config(relief=tk.SUNKEN)
            self.switch_on_replace.config(bg='red')
        else:
            self.switch_on_replace_var.set(0)
            self.switch_on_replace.config(relief=tk.RAISED)
            self.switch_on_replace.config(text='Off')
            self.switch_on_replace.config(bg='gray')

    def search_forward(self):
        self.parent.search_forward(self.search_text_var.get())
        if self.switch_on_replace_var.get() == 1:
            self.parent.replace_selected_text(self.replace_text_var.get())

    def search_backward(self):
        self.parent.search_backward(self.search_text_var.get())
        if self.switch_on_replace_var.get() == 1:
            self.parent.replace_selected_text(self.replace_text_var.get())
