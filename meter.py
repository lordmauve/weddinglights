import time
import random
from collections import deque

from btrack import track_beats
from lights import (
    Grid, hsv, WHITE,
    Spotlight
)


grid = Grid(interp=True)

vols = deque([0] * 50, maxlen=50)


with track_beats() as tracker:
    for f in grid.fps(30):
        vols.append(min(tracker.vol, 0.1) / 0.1)
        grid.clear()
        for x, v in enumerate(vols):
            whole, frac = divmod(v, 0.25)
            frac /= 0.25
            whole = int(whole)
            for y in range(4 - whole, 4 + whole):
                grid[x, y] = 0, 255, 0
            if whole < 4:
                c = 0, frac * 255, 0
                for y in (4 - whole - 1, 4 + whole):
                    grid[x, y] = c
