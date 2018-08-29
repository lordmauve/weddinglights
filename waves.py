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
        for x, y, vx, intensity in waves:
            rx = round(x)
            c = round(min(intensity, 1.0) * 255)
            grid[rx, y] = (c, c, c)
            if rx < x < grid.W - 1:
                grid[rx + 1, y] = (c * 2 * (x - rx),) * 3
            x += vx
            if x + 0.5 < grid.W:
                newwaves.append((x, y, vx, intensity * 0.98))
        waves = newwaves

        if tracker.has_beats():
            intensity = min(tracker.vol, 0.03) / 0.03
            for y in range(grid.H):
                waves.append((0, y, random.uniform(0.5, 0.55), intensity))
