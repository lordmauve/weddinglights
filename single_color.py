import time
import random
import readline

from grid import Grid
from colors import color_map

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


while True:
    while True:
        name = raw_input("Next color? ")
        try:
            color = colors[name]
        except KeyError:
            print("Invalid color")
        else:
            print("Great, {} is {}".format(name, color))
            break

    for p in grid.keys():
        grid[p] = color
    grid.flip()
