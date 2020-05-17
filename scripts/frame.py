'''
gduarte@astro.ufsc.br
Created on 15-mai-2020
'''

from tkinter import *

import glob

from scripts.game import *
from scripts.menus import *


WIDTH = 421
HEIGHT = 241

class App(Frame):
    def __init__(self, master):
        super().__init__(master, width=WIDTH, height=HEIGHT, 
                         bg='#93c000')
        self.main_menu = Menu(self)
        self.game = Game(self)
        self.main_menu.start()
        self.pack()

    def handle_function(self, entry):
        fun = {'new_game': self.start_game,
               'main_menu': self.open_main_menu}
        fun[entry]()

    def open_main_menu(self):
        self.game.pack_forget()
        self.main_menu.start()

    def start_game(self):
        self.main_menu.pack_forget()
        self.game.start()

    def close_app(self):
        self.master.destroy()


def main():
    root = Tk()
    game = App(root)
    root.mainloop()
