import tkinter as tk
import re
from pathlib import Path
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
        self.syntax_file_io = FileIO()

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

        self.editor.bind('<Button-3>', self.rClicker, add='')

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

    def set_editor_fgcolor(self, hex_color):
        self.editor['foreground'] = hex_color

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

    def toggle_wrap(self, on):
        if on == 1:
            self.editor['wrap'] = tk.WORD
        else:
            self.editor['wrap'] = tk.NONE

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

    def rClicker(self, e):
        ''' right click context menu for all Tk Entry and Text widgets
        '''

        try:
            def rClick_Copy(e, apnd=0):
                e.widget.event_generate('<Control-c>')

            def rClick_Cut(e):
                e.widget.event_generate('<Control-x>')

            def rClick_Paste(e):
                e.widget.event_generate('<Control-v>')

            def rClick_Highlight_Keyword(e):
                self.highlight_syntax(True)

            e.widget.focus()

            nclst = [
                (' Cut', lambda e=e: rClick_Cut(e)),
                (' Copy', lambda e=e: rClick_Copy(e)),
                (' Paste', lambda e=e: rClick_Paste(e)),
                (' Highlight Keyword', lambda e=e: rClick_Highlight_Keyword(e)),
            ]

            rmenu = tk.Menu(None, tearoff=0, takefocus=0)

            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)

            rmenu.tk_popup(e.x_root + 40, e.y_root + 10, entry="0")

        except tk.TclError:
            print
            ' - rClick menu, something wrong'
            pass

        return "break"

    def highlight_syntax(self, enable=True):
        syntax_file = Path(Path(self.file_io.file_name).suffix[1:]).with_suffix('.hs')
        hs_config_data = Configuration.get_hs_configuration(syntax_file)
        if hs_config_data is None:
            print('No syntax file ', syntax_file)
            return
        #print(hs_config_data)
        keywords = hs_config_data['keyword']['tags']
        keyword_fgcolor = hs_config_data['keyword']['color']
        constant_fgcolor = hs_config_data['constant']['color']

        numbers = re.findall(r'\d{1,3}', self.file_io.file_data)
        self.editor.tag_config('tg_kw', foreground=keyword_fgcolor)
        self.editor.tag_config('tg_num', foreground=constant_fgcolor)
        #keywords = ['package', 'public', 'private', 'abstract', 'internal', 'new', 'static', 'final', 'long', 'extends',
        #            'class', 'import', 'null', 'for', 'if', 'return', 'int', 'char', 'float', 'double', 'implements']
        for keyword in keywords:
            self.editor.mark_set(tk.INSERT, '1.0')
            while True:
                located_end = self.highlight_keyword(keyword+' ', 'tg_kw')
                if located_end == 0:
                    break
                self.editor.mark_set(tk.INSERT, located_end)

        self.editor.mark_set(tk.INSERT, '1.0')
        for each_number in numbers:
            located_end = self.highlight_keyword(each_number, 'tg_num')
            if located_end != 0:
                self.editor.mark_set(tk.INSERT, located_end)

        print("Syntax highlight executed.")

    def highlight_keyword(self, text, tag):
        located_start = self.editor.search(text, tk.INSERT, stopindex=tk.END, forwards=True, nocase=False)
        located_end = '{}+{}c'.format(located_start, len(text))
        print(located_start, ',', located_end)
        print('keyword', text)
        if located_start is '' or located_end is '':
            return 0

        self.editor.tag_add(tag, located_start, located_end)
        return located_end
