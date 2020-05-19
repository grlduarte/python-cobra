'''
gduarte@astro.ufsc.br
Created on 17-mai-2020
'''

import glob
from tkinter import *

from scripts.game_objects import *

class Game(Canvas):
    def __init__(self, master):
        self.master = master
        self.load_config()
        self.load_images()
        self.ingame = False
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
            options = f.readlines()
        self.level = int(options[0])
        self.maze = Maze(options[1])
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
            self.delete(ALL)
            self.load_options()
            self.dx, self.dy = 1, 0

            self.snake = Snake(self.columns, self.rows, self.maze)
            self.food = Food(self.columns, self.rows)
            self.food.draw()
            self.score = 0

            self.create_image((0, 0), anchor=NW, image=self.maze.frame)
            self.obj_tags = []
            self.score_tags = []
        self.step()

    def step(self):
        try:
            self.handling = False
            self.snake.crawl(self.dx, self.dy, food_pos=self.food)
            self.head_on_food()
            self.delete(*self.obj_tags)
            self.obj_img = ['food'] + self.snake.img
            self.obj_coords = [self.food] + self.snake.pos
            self.draw_objects()
            self.draw_score()
            self.ident = self.after(self.delay, self.step)
        except CollisionError:
            self.end_game()

    def head_on_food(self):
        if self.snake.pos[0] == self.food:
            self.move_food()
            self.score += 1

    def move_food(self):
        self.food.draw()
        while self.food in (self.snake.pos + self.maze.walls):
            self.food.draw()

    def draw_objects(self):
        self.tags = []
        for c, i in zip(self.obj_coords, self.obj_img):
            c = list(self.origin + self.dot_size * c)
            img = self.game_img[i]
            t = self.create_image(c, anchor=NW, image=img)
            self.obj_tags.append(t)

    def draw_score(self):
        self.delete(*self.score_tags)
        self.score_tags = []
        score = f'{self.level * self.score:04d}'
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
                self.draw_objects()
                self.after(300, draw)
            else:
                game_over()
        def game_over():
            self.delete(ALL)
            img = self.game_img['game_over']
            self.create_image([5, 0], anchor=NW, image=img)
            score = f'{self.level * self.score}'
            coords = [[5, 160], [45, 160], [85, 160], [125, 160]]
            for c, s in zip(coords, score):
                img = self.n_img['b'+s]
                self.create_image(c, anchor=NW, image=img)
            self.after(3000, go_to_menu)
        def go_to_menu():
            self.delete(ALL)
            self.master.handle_function(self, 'main_menu')
        draw()
