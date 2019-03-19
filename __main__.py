import os
import sys

import source.home_screen as home_screen
#from source.home_screen import Application
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.state('zoomed')
    root.title('eSya Text')
    home_screen.Application.APPLICATION_ROOT = os.path.dirname(sys.modules['__main__'].__file__)
    app_icon_path = os.path.join(home_screen.Application.APPLICATION_ROOT, 'source', 'image', 'application.gif')
    application_icon = tk.PhotoImage(file=app_icon_path)
    root.tk.call('wm', 'iconphoto', root._w, application_icon)
    # root.tk.call('tk', 'scaling', 2.0)
    app = home_screen.Application(master=root)
    app.mainloop()
