import  tkinter as tk


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
        self.search_text_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.container_frame = tk.LabelFrame(self.top, text='Search options', width=50)
        self.container_frame.pack(side="left", pady=(0, 3), padx=(3, 0))
        self.container_frame.pack(fill="y", expand=True)

        self.search_label = tk.Label(self.container_frame, text='Text')
        self.search_label.grid(row=0, column=0, pady=(10, 10), padx=(5, 5))

        self.search_text = tk.Entry(self.container_frame, width=40, textvariable=self.search_text_var)
        self.search_text.grid(row=0, column=1, pady=(10, 10), padx=(5, 10))
        self.search_text.focus()

        self.container_frame_btn = tk.LabelFrame(self.top, width=12, height=25)
        self.container_frame_btn.pack(side='right', pady=(3, 3), padx=(3, 3))

        search_backward__icon = tk.PhotoImage(file="source/image/search_backward.gif")
        self.search_back_btn = tk.Button(self.container_frame_btn, image=search_backward__icon,
                                         command=self.search_backward)
        self.search_back_btn.image = search_backward__icon
        self.search_back_btn.pack(side='top', pady=(5, 10), padx=(5, 5))

        search_forward__icon = tk.PhotoImage(file="source/image/search_forward.gif")
        self.search_next_btn = tk.Button(self.container_frame_btn, image=search_forward__icon,
                                         command=self.search_forward)
        self.search_next_btn.image = search_forward__icon
        self.search_next_btn.pack(side='bottom', pady=(10, 5), padx=(5, 5))

    def search_forward(self):
        self.parent.search_forward(self.search_text_var.get())

    def search_backward(self):
        self.parent.search_backward(self.search_text_var.get())
