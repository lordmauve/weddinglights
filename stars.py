import time
from itertools import count
import random
from collections import deque

from lights import Grid



grid = Grid()

rising = deque(maxlen=30)


for t in grid.fps(60):
    grid.darken(0.95)

    if t % 3 == 0:
        rising.append(grid.rand_pos())

    for pos in rising:
        if pos is None:
            continue
        grid[pos] = tuple(min(255, c + 20) for c in grid[pos])
