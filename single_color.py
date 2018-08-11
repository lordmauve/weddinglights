import sys
import time
import random
import readline

from lights import Grid, color_map

grid = Grid(interp=False)


colors = color_map()

def complete(name, state):
    matches = [k for k in colors if k.startswith(name)]
    try:
        return matches[state]
    except IndexError:
        return None


readline.parse_and_bind("tab: complete")
readline.set_completer(complete)


grid.flip()
last = 'black'
while True:
    while True:
        try:
            name = input(last + "> ")
        except EOFError:
            sys.exit(0)
        try:
            color = colors[name]
        except KeyError:
            print("Invalid color")
        else:
            print("Great, {} is {}".format(name, color))
            last = name
            break

    for p in grid.keys():
        grid[p] = color
    grid.fade()
