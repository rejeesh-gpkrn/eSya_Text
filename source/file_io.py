import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_messagebox


class FileIO:

    """File read and write activities."""

    def __init__(self):
        self.file_name = None
        self.file_data = None

    def read(self):
        self.file_name = tk_filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),
                                       ("All files", "*.*")))
        if self.file_name:
            with open(self.file_name, "r", encoding='EUC-JP') as file_read_handler:
                self.file_data = file_read_handler.read()
            return True
        else:
            tk_messagebox.showerror('Failed', 'No files are selected!!!')
            return False

    def save(self):
        if self.file_name is None:
            self.file_name = tk_filedialog.asksaveasfilename(filetypes = (("Text files", "*.txt"),
                                       ("All files", "*.*")))
            if self.file_name is None or self.file_name is '':
                tk_messagebox.showerror('Failed', 'No filename selected!!!')
                return
        if self.file_data is None:
            self.file_data = ''
        with open(self.file_name, "w") as file_write_handler:
            file_write_handler.write(self.file_data)
