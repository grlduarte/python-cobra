'''
gduarte@astro.ufsc.br
Created on 17-mai-2020
'''

import glob
from tkinter import *

from scripts.grid import *


DELAY = 400

class Game(Canvas):
    def __init__(self, master):
        self.master = master
        self.load_config()
        self.load_images()
        super().__init__(master, bg='#93c000',
                         width=self.width, height=self.height)

    def load_config(self):
        # Columns and rows as the original Snake II game
        # Dot size defined as the size of the images
        self.columns = 20
        self.rows = 9
        self.dot_size = 20
        self.width = self.master['width']
        self.height = self.master['height']
        self.origin = Vector(10, 50)

    def load_options(self):
        delay_map = {1: 650, 2: 500, 3: 375,
                     4: 300, 5: 225, 6: 185,
                     7: 135, 8: 115, 9: 90}
        with open('options', 'r') as f:
            self.options = f.readlines()
        self.level = int(self.options[0])
        self.maze = self.options[1]
        self.delay = delay_map[self.level]

    def load_images(self):
        image_list = glob.glob('img/game/*')
        self.game_img = {}
        self.game_img['_'] = None
        for i in image_list:
            k = i.replace('img/game/', '').replace('.xbm', '')
            self.game_img[k] = BitmapImage(file=i)

        image_list = glob.glob('img/numbers/*')
        self.n_img = {}
        for i in image_list:
            k = i.replace('img/numbers/', '').replace('.xbm', '')
            self.n_img[k] = BitmapImage(file=i)

    def handle_key(self, event):
        key = event.keysym

        if not self.handling and self.ingame:
            if key == 'Up' and self.dy == 0:
                self.handling = True
                self.dx = 0
                self.dy = -1

            elif key == 'Down' and self.dy == 0:
                self.handling = True
                self.dx= 0
                self.dy = 1

            elif key == 'Left' and self.dx == 0:
                self.handling = True
                self.dx = -1
                self.dy = 0

            elif key == 'Right' and self.dx == 0:
                self.handling = True
                self.dx = 1
                self.dy = 0

            elif key == 'Escape':
                self.after_cancel(self.ident)
                self.master.handle_function(self, 'main_menu', onpause=self.ingame)

    def start(self, resuming=False):
        self.pack(side=TOP)
        self.bind_all('<Key>', self.handle_key)
        self.ingame = True
        
        if not resuming:
            self.load_options()
            self.delete(ALL)
            self.dx, self.dy = 1, 0
            self.board = Grid(self.columns, self.rows, self.dot_size)
            self.create_image((0, 0), anchor=NW, image=self.game_img['frame'])
            self.obj_tags = []
            self.score_tags = []
        self.step()

    def step(self):
        try:
            self.handling = False
            self.board.step(self.dx, self.dy)
            self.delete(*self.obj_tags)
            self.draw_grid()
            self.draw_score()
            self.ident = self.after(self.delay, self.step)
        except CollisionError:
            self.end_game()

    def draw_grid(self):
        self.tags = []
        for sq in self.board:
            coords = list(self.origin + sq.coords[:2])
            img = self.game_img[sq.obj]
            t = self.create_image(coords, anchor=NW, image=img)
            self.obj_tags.append(t)

    def draw_score(self):
        self.delete(*self.score_tags)
        self.score_tags = []
        score = f'{self.level * self.board.score:04d}'
        coords = [[0, 0], [20, 0], [40, 0], [60, 0]] 
        for c, s in zip(coords, score):
            img = self.n_img['n'+s]
            t = self.create_image(c, anchor=NW, image=img)
            self.score_tags.append(t)

    def end_game(self):
        self.ingame = False
        self.blink_count = 0
        def draw():
            self.blink_count += 1
            self.delete(*self.obj_tags)
            self.after(300, clear)
        def clear():
            if self.blink_count < 5:
                self.draw_grid()
                self.after(300, draw)
            else:
                game_over()
        def game_over():
            self.delete(ALL)
            img = self.game_img['game_over']
            self.create_image([5, 0], anchor=NW, image=img)
            score = f'{self.level * self.board.score}'
            coords = [[5, 160], [45, 160], [85, 160], [125, 160]]
            for c, s in zip(coords, score):
                img = self.n_img['b'+s]
                self.create_image(c, anchor=NW, image=img)
            self.after(3000, go_to_menu)
        def go_to_menu():
            self.delete(ALL)
            self.master.handle_function(self, 'main_menu')
        draw()
##############################################


