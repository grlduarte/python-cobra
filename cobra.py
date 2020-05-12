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
        self.master = master
        super().__init__(master, bg=self.color_background,
                         width=self.width, height=self.height)

        self.bind_all('<Key>', self.handle_key)
        self.run()
        self.pack()


    def load_config(self, config_file):
        self.width = 300
        self.height = 300
        self.dot_size = 10
        self.initial_length = 5
        self.columns = int(self.width / self.dot_size)
        self.rows = int(self.height / self.dot_size)

        self.time_step = {1: 500, 2: 350, 3: 200,
                          4: 100, 5: 50, 6: 30}

        config = configparser.ConfigParser()
        config.read(config_file)
        for cfg in config['GENERAL']:
            setattr(self, cfg, int(config['GENERAL'][cfg]))
        for cfg in config['COLOR']:
            setattr(self, 'color_'+cfg, config['COLOR'][cfg])

        self.delay = self.time_step[self.level]
        self.obstacles = []


    def rect_coords(self, x, y):
        return (x, y, x+self.dot_size, y+self.dot_size)


    def handle_key(self, event):
        key = event.keysym

        if key == 'q':
            self.master.destroy()

        if self.running:
            if self.alive:
                if key == 'Up' and self.dy == 0:
                    self.dx = 0
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
            
        elif self.alive:
            self.running = True
            self.ident = self.after(self.delay, self.step)

        else:
            if key == 'r':
                self.delete(tk.ALL)
                self.run()


    def run(self):
        '''Set initial parameters and starts the game'''
        self.alive = True
        self.running = False
        self.score = 0

        self.dx, self.dy = self.dot_size, 0
        self.draw_snake()

        self.place_food(first=True)
        self.ident = self.after(self.delay, self.step)


    def draw_snake(self):
        '''Draws the snake at the initial state'''
        x1, y1, x2, y2 = self.rect_coords(self.width // 2, self.height // 2)
        self.length = self.initial_length

        self.create_rectangle(x1, y1, x2, y2, fill=self.color_snake, tag='head')
        for i in range(self.length):
            tag = f'dot{i}'
            x1, x2 = x1 - self.dx, x2 - self.dx
            self.create_rectangle(x1, y1, x2, y2, fill=self.color_snake, tag=tag)


    def step(self):
        '''Function for each time step of the game'''
        self.check_collision()
        if self.alive and self.running:
            self.move_snake()
            self.ident = self.after(self.delay, self.step)


    def check_collision(self):
        '''Checks if the head of the snake collides with itself or some obstacle'''
        head = self.coords('head')[:2]
        body = [self.coords(f'dot{i}')[:2] for i in range(self.length)]
        
        if (head in body):
            self.die()


    def move_snake(self):
        '''
        Move the head of the snake then place each of the 
        following squares at the position of the next one
        '''
        if self.coords('head') == self.coords('food'):
            self.eat_food()

        x, y = self.move_head()
        for i in range(self.length):
            tag = f'dot{i}'
            x, y = self.move_body(tag, x, y)


    def move_head(self):
        '''Moves the head of the snake'''
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
        '''Place food in a random place of the board'''
        x, y = np.random.randint((0, 0), (self.columns, self.rows), 2)
        coords = self.rect_coords(self.dot_size*x, self.dot_size*y)
        
        head = self.coords('head')[:2]
        body = [self.coords(f'dot{i}')[:2] for i in range(self.length)]
        while coords in (head + body):
            x, y = np.random.randint((0, 0), (self.columns, self.rows), 2)
            coords = self.rect_coords(self.dot_size*x, self.dot_size*y)

        if first:
            self.create_rectangle(coords, fill='red', tag='food')
        else:
            x, y = coords[:2]
            self.moveto('food', x-1, y-1)


    def eat_food(self):
        '''Increase score and size of the snake'''
        self.place_food()
        if self.score == 0:
            coords = self.coords('head')
        else:
            coords = self.coords(f'dot{self.length-1}')

        self.create_rectangle(coords, fill=self.color_snake, tag=f'dot{self.length}')
        self.score += self.level
        self.length += 1


    def die(self):
        self.alive = False
        self.running = False
        self.after_cancel(self.ident)
        print(f"Game over: {self.score}")
