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
        self.main_menu = MainMenu(self)
        self.level_menu = LevelMenu(self)
        self.mazes_menu = MazesMenu(self)
        self.game = Game(self)

        self.main_menu.start()
        self.pack()

    def handle_function(self, caller, entry, **kw):
        fun = {'new_game': self.start_game,
               'continue': self.resume_game,
               'main_menu': self.open_main_menu,
               'level': self.open_level_menu,
               'mazes': self.open_mazes_menu,
               'top_scores': self.open_top_score_menu}
        fun[entry](caller, **kw)

    def open_main_menu(self, caller, onpause=False):
        caller.pack_forget()
        if onpause:
            self.main_menu.add_item('continue')
        else:
            self.main_menu.remove_item('continue')
        self.main_menu.start()

    def start_game(self, caller, **kw):
        caller.pack_forget()
        self.game.start()

    def resume_game(self, caller):
        caller.pack_forget()
        self.game.start(resuming=True)

    def open_level_menu(self, caller):
        caller.pack_forget()
        self.level_menu.start()

    def open_mazes_menu(self, caller):
        caller.pack_forget()
        self.mazes_menu.start()

    def open_top_score_menu(self, caller):
        pass

    def unpack_all(self):
        for w in self.pack_slaves():
            w.pack_forget()

    def close_app(self):
        self.master.destroy()


def main():
    root = Tk()
    game = App(root)
    root.mainloop()
