'''
gduarte@astro.ufsc.br
Created on 16-mai-2020
'''

from tkinter import *
import glob

class Menu(Canvas):
    def __init__(self, master):
        self.master = master
        self.items = []
        self.load_images()
        self.item_coords = [[0, 30], [0, 85],
                            [0, 140], [0, 190]]
        super().__init__(master,
                         bg=self.master['bg'],
                         width=self.master['width'],
                         height=self.master['height'])

    def load_images(self):
        image_list = glob.glob('img/numbers/*')
        self.n_img = {}
        for i in image_list:
            k = i.replace('img/numbers/', '').replace('.xbm', '')
            self.n_img[k] = BitmapImage(file=i)

        image_list = glob.glob('img/menus/*')
        self.menu_img = {}
        for i in image_list:
            k = i.replace('img/menus/', '').replace('.xbm', '')
            self.menu_img[k] = BitmapImage(file=i)

    def handle_key(self, event):
        key = event.keysym

        if self.active:
            if key == 'Up':
                self.menu_up()

            elif key == 'Down':
                self.menu_down()

            elif key == 'Return':
                self.handle_return()

            elif key == 'Escape':
                self.handle_escape()

    def start(self):
        self.pack(side=TOP)
        self.bind_all('<Key>', self.handle_key)
        self.active = True
        self.start_routine()

        self.pointer = 0
        self.scroll = 0
        self.scroll_lim = len(self.items) - 3
        self.display_menu()

    def start_routine(self):
        pass

    def display_menu(self):
        self.delete(ALL)

        self.displayed = self.items[self.scroll:self.scroll+3]
        self.highlighted = self.displayed[self.pointer]
        self.displayed += ['select']
        for c, i in zip(self.item_coords, self.displayed):
            if i == self.displayed[self.pointer]:
                img = self.menu_img[i + '_sel']
            else:
                img = self.menu_img[i]
            self.create_image(c, anchor=NW, image=img)

    def menu_up(self):
        self.pointer -= 1
        if self.pointer < 0:
            self.pointer = 0
            self.scroll -= 1
            if self.scroll < 0:
                self.pointer = 2
                self.scroll = self.scroll_lim
        self.display_menu()

    def menu_down(self):
        self.pointer += 1
        if self.pointer > 2:
            self.pointer = 2
            self.scroll += 1 
            if self.scroll > self.scroll_lim:
                self.pointer = 0
                self.scroll = 0
        self.display_menu()

    def add_item(self, item):
        if not (item in self.items):
            self.items = [item] + self.items
            self.scroll_lim = len(self.items) - 3

    def remove_item(self, item):
        try:
            self.items.remove(item)
            self.scroll_lim = len(self.items) - 3
        except ValueError:
            pass


class MainMenu(Menu):
    def __init__(self, master):
        super().__init__(master)
        self.items = ['new_game', 'level', 'mazes',
                      'top_scores', 'instructions',
                      'settings']

    def handle_return(self):
        self.active = False
        self.master.handle_function(self, self.highlighted)

    def handle_escape(self):
        self.active = False
        self.master.close_app()


class MazesMenu(Menu):
    def __init__(self, master):
        super().__init__(master)
        self.items = ['no_maze', 'box', 'tunnel',
                      'spiral', 'blockade', 'twisted']

    def start_routine(self):
        with open('options', 'r') as f:
            self.options = f.readlines()

    def handle_return(self):
        self.active = False
        if self.options[1].strip() == self.highlighted:
            self.master.handle_function(self, 'main_menu',
                                        onpause=self.master.game.ingame)
        else:
            self.options[1] = self.highlighted
            with open('options', 'w') as f:
                f.writelines(self.options)
            self.master.handle_function(self, 'main_menu')

    def handle_escape(self):
        self.active = False
        self.master.handle_function(self, 'main_menu',
                                    onpause=self.master.game.ingame)


class LevelMenu(Canvas):
    def __init__(self, master):
        self.master = master
        self.load_images()
        super().__init__(master,
                         bg=self.master['bg'],
                         width=self.master['width'],
                         height=self.master['height'])

    def load_images(self):
        image_list = glob.glob('img/level_menu/*')
        self.level_img = {}
        for i in image_list:
            k = i.replace('img/level_menu/', '').replace('.xbm', '')
            self.level_img[k] = BitmapImage(file=i)

    def handle_key(self, event):
        key = event.keysym

        if self.active:
            if key == 'Up' or key == 'Right':
                self.menu_up()

            elif key == 'Down' or key == 'Left':
                self.menu_down()

            elif key == 'Return':
                self.active = False
                self.options[0] = str(self.level)
                with open('options', 'w') as f:
                    f.write('\n'.join(self.options))
                self.master.handle_function(self, 'main_menu')

            elif key == 'Escape':
                self.active = False
                self.master.handle_function(self, 'main_menu',
                                            onpause=self.master.game.ingame)

    def start(self):
        self.pack(side=TOP)
        self.bind_all('<Key>', self.handle_key)
        self.active = True

        with open('options', 'r') as f:
            self.options = f.readlines()
        self.level = int(self.options[0])
        self.display_menu()

    def display_menu(self):
        self.delete(ALL)
        img = self.level_img[f'level{self.level}']
        self.create_image([0, 0], anchor=NW, image=img)

    def menu_up(self):
        self.level += 1
        if self.level > 9:
            self.level = 9
        self.display_menu()

    def menu_down(self):
        self.level -= 1
        if self.level < 1:
            self.level = 1
        self.display_menu()
