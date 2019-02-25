import source.home_screen as home_screen
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.state('zoomed')
    root.title('eSya Text')
    # root.tk.call('tk', 'scaling', 1.0)
    app = home_screen.Application(master=root)
    app.mainloop()
