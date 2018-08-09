import time
import random

from grid import Grid
from colors import hsv



grid = Grid()

rising = [None] * 60


for f in grid.fps(40):
    for x, y in grid.keys():
        grid[x, y] = hsv(360 / 50 * (x + f))
