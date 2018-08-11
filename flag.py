import time
from lights import Grid, RED, WHITE, GREEN, BLACK

from itertools import count


COLORS = [RED, WHITE, GREEN, BLACK]

grid = Grid()
for t in grid.fps(2):
    for x, y in grid.keys():
        grid[x, y] = COLORS[(x + t) // 4 % len(COLORS)]
