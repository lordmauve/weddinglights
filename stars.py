import time
from itertools import count
import random

from lights import Grid, WHITE, YELLOW



grid = Grid()

rising = [None] * 60


for _ in grid.fps(30):
    for (x, y), v in grid.items():
        grid[x, y] = tuple(max(c - 5, 0) for c in v)

    rising[random.randrange(len(rising))] = grid.rand_pos()

    for pos in rising:
        if pos is None:
            continue
        grid[pos] = tuple(min(255, c + 10) for c in grid[pos])
