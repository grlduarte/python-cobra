'''
gduarte@astro.ufsc.br
Created on 12-mai-2020
'''

from cobra import *


def main():
    root = tk.Tk()
    scoreboard = TopBoard(root)
    levelboard = BottomBoard(root)
    game = Game(root, scoreboard, levelboard)
    root.mainloop()


if __name__ == '__main__':
    main()
