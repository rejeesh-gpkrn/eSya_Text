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

    def read(self, external_file_name = None):
        if external_file_name is None:
            self.file_name = tk_filedialog.askopenfilename(filetypes=(("All files", "*.*"),
                                                                  ("Text files", "*.txt")))
        else:
            self.file_name = external_file_name

        if self.file_name:
            self.detect_encoding()
            #self.encoding = Configuration.common['encoding'] if 'encoding' in Configuration.common else 'UTF8'
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
                value_error = ValueError('Empty file name.')
                return value_error
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

    def detect_encoding(self):
        supported_encodings = ['UTF8', 'EUC-JP', 'UTF16', 'latin_1']

        if 'encoding' in Configuration.common:
            self.encoding = Configuration.common['encoding']
            return

        for encoding_name in supported_encodings:
            try:
                with open(self.file_name, "r", encoding=encoding_name) as file_read_handler:
                    first_line = file_read_handler.readline()
                    self.encoding = encoding_name
                    print(self.encoding, self.file_name)
                    break;
            except:
                self.encoding = None
                pass
