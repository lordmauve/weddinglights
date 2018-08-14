import time
import random

from btrack import track_beats
from lights import (
    Grid, hsv, RED, CYAN, YELLOW, GREEN, PURPLE, BLUE, WHITE, BLACK,
    Block, Spotlight
)


grid = Grid(interp=True)

waves = []


with track_beats() as tracker:
    for f in grid.fps(60):
        grid.darken((0.6, 0.7, 0.9))
        newwaves = []
        for x, y, vx in waves:
            rx = round(x)
            grid[rx, y] = WHITE
            if rx < x < grid.W - 1:
                grid[rx + 1, y] = (255 * 2 * (x - rx),) * 3
            x += vx
            if x + 0.5 < grid.W:
                newwaves.append((x, y, vx))
        waves = newwaves

        if tracker.has_beats():
            for y in range(grid.H):
                waves.append((0, y, random.uniform(0.5, 0.55)))
