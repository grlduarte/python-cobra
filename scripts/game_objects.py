'''
gduarte@astro.ufsc.br
Created on 15-mai-2020
'''

from random import randint
from tkinter import BitmapImage


class CollisionError(Exception):
    pass


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __getitem__(self, idx):
        if idx == 0:
            out = self.x
        elif idx == 1:
            out = self.y
        else:
            raise IndexError
        return out

    def __setitem__(self, idx, value):
        if idx == 0:
            self.x = value
        elif idx == 1:
            self.y = value
        else:
            raise IndexError

    def __sub__(self, value):
        x = self[0] - value[0]
        y = self[1] - value[1]
        return Vector(x, y)

    def __add__(self, value):
        x = self[0] + value[0]
        y = self[1] + value[1]
        return Vector(x, y)

    def __mul__(self, value):
        x = value * self[0]
        y = value * self[1]
        return Vector(x, y)

    def __rmul__(self, value):
        return self.__mul__(value)

    def __eq__(self, value):
        x = self[0] == value[0]
        y = self[1] == value[1]
        return x and y

    @staticmethod
    def from_string(string):
        x, y = string.replace('(', '').replace(')', '').split(',')
        return Vector(int(x), int(y))


class Snake:
    def __init__(self, x_range, y_range, maze):
        self.directions = {(1, 0): 'right',
                           (-1, 0): 'left',
                           (0, 1): 'down',
                           (0, -1): 'up'}

        self.x_range = x_range
        self.y_range = y_range

        self.size = maze.size
        self.pos = [maze.p0 - (1, 0)]
        self.walls = maze.walls

        self.vel = [Vector(1, 0)]
        self.dir = [self.directions[(1, 0)]]
        self.food = ['']
        for i in range(1, self.size+1):
            self.pos += [self.pos[0] - i*self.vel[0]]
            self.vel += [Vector(1, 0)]
            self.dir += [self.directions[(self.vel[i][0], self.vel[i][1])]]
            self.food += ['']
        self.img = self.dir.copy()
        self.crawl(1, 0, (0, 0))

    def __getitem__(self, idx):
        item = [self.pos[idx], self.img[idx]]
        return item

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        try:
            out = self[self.i]
            self.i += 1
            return out
        except IndexError:
            raise StopIteration

    def update_attributes(self, dx, dy, food_pos):
        '''
        Coloca no comeco de todas as listas um atributo de
        acordo com dx e dy recebidos e depois apaga o ultimo
        item dessas listas, exceto se houver comida no ultimo
        item. Nesse caso, a cobra cresce em um quadrado.
        '''
        vel = [Vector(dx, dy)]
        self.vel = vel + self.vel

        pos = [self.pos[0] + self.vel[0]]
        self.pos = pos + self.pos
        self.end_of_board()

        direction = [self.directions[(dx, dy)]]
        self.dir = direction + self.dir

        if self.pos[0] == food_pos:
            food = ['_food']
        else:
            food = ['']
        self.food = food + self.food
        self.pop_last_item()

    def end_of_board(self):
        x, y = self.pos[0]
        if x > (self.x_range - 1):
            x = 0
        elif y > (self.y_range - 1):
            y = 0
        elif x < 0:
            x = self.x_range - 1
        elif y < 0:
            y = self.y_range - 1
        self.pos[0] = Vector(x, y)

    def pop_last_item(self):
        if self.food[-2] == '_food':
            self.food[-2] = ''
        if self.food[1] == '_food':
            self.size += 1
        else:
            self.vel.pop()
            self.pos.pop()
            self.dir.pop()
            self.food.pop()

    def set_images(self, food_pos):
        img = self.dir.copy()
        if (self.pos[0] + self.vel[0]) == food_pos:
            img[0] += '_open'

        for i in range(1, len(self.img)):
            if not (self.dir[i-1] == self.dir[i]):
                img[i] = self.dir[i] + '_' + self.dir[i-1]
            img[i] += self.food[i]

        img[0] = 'head_' + img[0]
        img[-1] = 'tail_' + img[-1]
        self.img = img

    def crawl(self, dx, dy, food_pos):
        self.check_collision(dx, dy)
        self.update_attributes(dx, dy, food_pos)
        self.set_images(food_pos)

    def check_collision(self, dx, dy):
        if (self.pos[0] + Vector(dx, dy)) in (self.pos[1:] + self.walls):
            raise CollisionError


class Food(Vector):
    def __init__(self, *args):
        self.x_range = args[0]
        self.y_range = args[1]
        self.draw()

    def draw(self):
        self.x = randint(0, self.x_range - 1)
        self.y = randint(0, self.y_range - 1)


class Maze:
    def __init__(self, name):
        self.name = name
        path = f'mazes/{name}'
        with open(f'{path}.mze', 'r') as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]

        self.highscore = int(lines[0])
        self.p0 = Vector.from_string(lines[1])
        self.size = int(lines[2])
        self.frame = BitmapImage(file=f'{path}.xbm')
        obstacles = []
        try:
            for wall in lines[3:]:
                wall = wall.replace('(', '').replace(')', '')
                p0, pf, d = wall.split('->')
                p0 = Vector.from_string(p0)
                pf = Vector.from_string(pf)
                d = Vector.from_string(d)
                i = 0
                while True:
                    obstacles.append(p0 + i*d)
                    i += 1
                    if obstacles[-1] == pf:
                        break
        except IndexError:
            pass
        self.walls = obstacles
