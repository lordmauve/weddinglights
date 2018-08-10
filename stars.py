import time
from itertools import count
import random
from collections import deque

from lights import Grid



grid = Grid()

rising = deque(maxlen=30)


for t in grid.fps(60):
    for (x, y), v in grid.items():
        grid[x, y] = tuple(max(c - 5, 0) for c in v)

    if t % 5 == 0:
        rising.append(grid.rand_pos())

    for pos in rising:
        if pos is None:
            continue
        grid[pos] = tuple(min(255, c + 10) for c in grid[pos])
