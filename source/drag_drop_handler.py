
class DragDropHandler:
    '''Clas for supporting dropping file'''

    def __init__(self, widget=None):
        self.widget = widget
        self.key_binding()
        print('DragDropHandler initialized')

    def key_binding(self):
        self.widget.bind("<ButtonPress-1>", self.on_start)
        self.widget.bind("<B1-Motion>", self.on_drag)
        self.widget.bind("<ButtonRelease-1>", self.on_drop)
        #self.widget.configure(cursor="hand1")
        #self.master.protocol('WM_DELETE_WINDOW', self.on_delete_window)
        #self.master.bind("<Control-s>", self.control_s)

    def on_start(self, event):
        pass

    def on_drag(self, event):
        pass

    def on_drop(self, event):
        #x, y = event.widget.winfo_pointerxy()
        #target = event.widget.winfo_containing(x, y)
        try:
            print('on-drop', event)
            #target.configure(image=event.widget.cget("image"))
        except:
            pass
