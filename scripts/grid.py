'''
gduarte@astro.ufsc.br
Created on 13-mai-2020
'''

from scripts.objects import *

class GridSquare:
    def __init__(self, x, y, sq_size, **kw):
        self.grid_coords = [x, y]
        self.coords = [sq_size*x, sq_size*y,
                       sq_size*(x+1), sq_size*(y+1)]
        self.obj = '_'
        for k in kw:
            setattr(self, k, kw[k])


class Grid:
    def __init__(self, x_size, y_size, step):
        self.x_size = int(x_size)
        self.y_size = int(y_size)
        self.grid_step = step
        self.snake = Snake([x_size//2, y_size//2], x_size, y_size)
        self.food = Food(x_size, y_size)
        self.score = 0
        self.items = self.snake.pos + [self.food]
        self.move_food()
        grid = []
        for j in range(self.y_size):
            grid.append([GridSquare(i, j, self.grid_step) for i in range(x_size)])
        self.grid = grid

    def __getitem__(self, idx):
        x, y = idx
        item = self.grid[y][x]
        return item

    def __setitem__(self, idx, value):
        x, y = idx
        self.grid[y][x] = value

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.items):
            out = self[self.items[self.i]]
            self.i += 1
            return out
        else:
            raise StopIteration

    def step(self, dx, dy):
        self.snake.crawl(dx, dy, food_pos=self.food)
        self.head_on_food()
        self.clean()
        self.place_objects()
        self.items = self.snake.pos + [self.food]

    def clean(self):
        for sq in self:
            sq.obj = '_'

    def head_on_food(self):
        if self.snake.pos[0] == self.food:
            self.move_food()
            self.score += 1

    def move_food(self):
        self.food.draw()
        while self.food in self.snake.pos:
            self.food.draw()

    def place_objects(self):
        self[self.food].obj = 'food'
        for s in self.snake:
            self[s[0]].obj = s[1]

    def find_object(self, obj, n=-1):
        out = []
        i = 0
        for sq in self:
            if i == n:
                break
            if sq.obj == obj:
                out.append(sq.grid_coords)
                i += 1
        return out
