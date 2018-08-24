import time
import random

from btrack import track_beats
from lights import (
    Grid, hsv, WHITE,
    Spotlight
)


grid = Grid(interp=True)

spot = Spotlight(grid, 0, 0, 16, 8)
pos = 58


with track_beats() as tracker:
    for f in grid.fps(60):
        pos -= 0.5
        if pos < -8:
            pos = 58

        fade_col = hsv(f / 10)
        grid.darken(tuple(0.85 + 0.1 * (c / 255) for c in fade_col))

        spot.x = round(pos)
        spot.intensity *= 0.93

        if tracker.has_beats():
            spot.intensity = 1.0
        spot.set(WHITE)
