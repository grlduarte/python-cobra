'''
gduarte@astro.ufsc.br
Created on 16-mai-2020
'''

from tkinter import *
import glob

WIDTH = 421
HEIGHT = 241

class Menu(Canvas):
    def __init__(self, master):
        self.master = master
        self.load_config()
        self.load_images()
        super().__init__(master, bg='#93c000',
                         width=self.width, height=self.height)

    def load_config(self):
        self.width = self.master['width']
        self.height = self.master['height']

    def load_images(self):
        image_list = glob.glob('img/numbers/*')
        self.n_img = {}
        for i in image_list:
            k = i.replace('img/numbers/', '').replace('.xbm', '')
            self.n_img[k] = BitmapImage(file=i)

        image_list = glob.glob('img/menu/*')
        self.menu_img = {}
        for i in image_list:
            k = i.replace('img/menu/', '').replace('.xbm', '')
            self.menu_img[k] = BitmapImage(file=i)

    def handle_key(self, event):
        key = event.keysym

        if self.active:
            if key == 'Up':
                self.menu_up()

            elif key == 'Down':
                self.menu_down()

            elif key == 'Return':
                self.active = False
                opt = self.displayed[self.highlight]
                self.master.handle_function(opt)

            elif key == 'Escape':
                self.master.close_app()

    def start(self):
        self.pack(side=TOP)
        self.bind_all('<Key>', self.handle_key)
        self.active = True

        self.highlight = 0
        self.scroll = 0
        self.menu_tag = []
        self.display_menu()

    def display_menu(self):
        self.delete(*self.menu_tag)
        self.menu_tag = []

        items = ['new_game', 'level', 'mazes', 'top_scores', 'instructions', 'settings']
        displayed = items[self.scroll:self.scroll+3] + ['select']
        coords = [[0, 30], [0, 85], [0, 140], [0, 190]]
        for c, i in zip(coords, displayed):
            if i == displayed[self.highlight]:
                img = self.menu_img[i + '_sel']
            else:
                img = self.menu_img[i]
            t = self.create_image(c, anchor=NW, image=img)
            self.menu_tag.append(t)
        self.displayed = displayed

    def menu_up(self):
        self.highlight -= 1
        if self.highlight < 0:
            self.highlight = 0
            self.scroll -= 1
            if self.scroll < 0:
                self.highlight = 2
                self.scroll = 3
        self.display_menu()

    def menu_down(self):
        self.highlight += 1
        if self.highlight > 2:
            self.highlight = 2
            self.scroll += 1 
            if self.scroll > 3:
                self.highlight = 0
                self.scroll = 0
        self.display_menu()

