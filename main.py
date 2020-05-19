'''
gduarte@astro.ufsc.br
Created on 12-mai-2020
'''

from tkinter import *

from scripts.frame import App

def main():
    root = Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.title('Snake II on Python')
    root.mainloop()


if __name__ == '__main__':
    main()
