'''
gduarte@astro.ufsc.br
Created on 08-mai-2020
'''

import configparser
import tkinter as tk

import numpy as np


class Game(tk.Canvas):
    def __init__(self, master=None, config_file='defaults.cfg'):
        self.load_config(config_file)
        super().__init__(master, bg=self.color_background,
                         width=self.width, height=self.height)

        self.bind_all('<Key>', self.handle_key)
        self.run()
        self.pack()


    def load_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        for cfg in config['GENERAL']:
            setattr(self, cfg, int(config['GENERAL'][cfg]))
        for cfg in config['COLOR']:
            setattr(self, 'color_'+cfg, config['COLOR'][cfg])

        self.columns = int(self.width / self.dot_size)
        self.rows = int(self.height / self.dot_size)

        self.delay = 200


    def rect_coords(self, x, y):
        return (x, y, x+self.dot_size, y+self.dot_size)


    def handle_key(self, event):
        key = event.keysym
        if self.running:
            if key == 'Up' and self.dy == 0:
                self.dx = 1
                self.dy = -self.dot_size

            elif key == 'Down' and self.dy == 0:
                self.dx= 0
                self.dy = self.dot_size

            elif key == 'Left' and self.dx == 0:
                self.dx = -self.dot_size
                self.dy = 0

            elif key == 'Right' and self.dx == 0:
                self.dx = self.dot_size
                self.dy = 0

            elif key == 'Escape':
                self.running = False
                self.after_cancel(self.ident)
            
        else:
            self.running = True
            self.ident = self.after(self.delay, self.draw_screen)


    def run(self):
        self.alive = True
        self.running = True
        self.score = 0

        self.dx, self.dy = 0, 0
        coords = self.rect_coords(self.width // 2, self.height // 2)
        self.create_rectangle(coords, fill=self.color_snake, tag='head')

        self.place_food(first=True)
        self.ident = self.after(self.delay, self.draw_screen)


    def draw_screen(self):
        self.check_collision()
        if self.alive and self.running:
            if self.coords('head') == self.coords('food'):
                self.eat_food()

            x, y = self.move_head()
            for i in range(self.score):
                tag = f'dot{i}'
                x, y = self.move_body(tag, x, y)

            self.ident = self.after(self.delay, self.draw_screen)


    def check_collision(self):
        head = self.coords('head')[:2]
        body = [self.coords(f'dot{i}')[:2] for i in range(self.score)]
        if (head in body) and (self.score > 0):
            self.die()


    def move_head(self):
        tag = 'head'
        xold, yold = self.coords(tag)[:2]

        self.move(tag, self.dx, self.dy)
        x, y = self.coords(tag)[:2]
        if x < 0:
            self.move(tag, self.width, 0)
        elif x > self.width-self.dot_size:
            self.move(tag, -self.width, 0)
        elif y < 0:
            self.move(tag, 0, self.height)
        elif y > self.height-self.dot_size:
            self.move(tag, 0, -self.height)
        return xold, yold


    def move_body(self, tag, x, y):
        xold, yold = self.coords(tag)[:2]
        # For some reason, moveto moves to coords+1
        self.moveto(tag, x-1, y-1)
        return xold, yold


    def place_food(self, first=False):
        x, y = np.random.randint((0, 0), (self.columns, self.rows), 2)
        coords = self.rect_coords(self.dot_size*x, self.dot_size*y)
        if first:
            self.create_rectangle(coords, fill='red', tag='food')
        else:
            x, y = coords[:2]
            self.moveto('food', x-1, y-1)


    def eat_food(self):
        self.place_food()
        if self.score == 0:
            coords = self.coords('head')
        else:
            coords = self.coords(f'dot{self.score-1}')

        self.create_rectangle(coords, fill=self.color_snake, tag=f'dot{self.score}')
        self.score += 1


    def die(self):
        self.alive = False
        print(f"Game over: {self.score}")
