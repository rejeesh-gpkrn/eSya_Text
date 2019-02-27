import sys
import tkinter.filedialog as tk_filedialog
import tkinter.messagebox as tk_messagebox

from source.configuration import Configuration


class FileIO:

    """File read and write activities."""

    def __init__(self):
        self.file_name = None
        self.file_data = None
        self.encoding = None

    def read(self):
        self.file_name = tk_filedialog.askopenfilename(filetypes=(("All files", "*.*"),
                                                                  ("Text files", "*.txt")))
        if self.file_name:
            self.encoding = Configuration.common['encoding'] if 'encoding' in Configuration.common else 'UTF8'
            try:
                with open(self.file_name, "r", encoding=self.encoding) as file_read_handler:
                    self.file_data = file_read_handler.read()
                return None
            except:
                return sys.exc_info()
        else:
            value_error = ValueError('Empty file name.')
            return value_error

    def save(self):
        if self.file_name is None or self.file_name is '':
            self.file_name = tk_filedialog.asksaveasfilename(filetypes=(("All files", "*.*"),
                                                                          ("Text files", "*.txt")))
            if self.file_name is None or self.file_name is '':
                tk_messagebox.showerror('Failed', 'No filename selected!!!')
                return
        if self.file_data is None:
            self.file_data = ''
        if self.encoding is None:
            self.encoding = Configuration.common['encoding'] if 'encoding' in Configuration.common else 'UTF8'
        try:
            with open(self.file_name, "w", encoding=self.encoding) as file_write_handler:
                file_write_handler.write(self.file_data)
            return None
        except:
            return sys.exc_info()
