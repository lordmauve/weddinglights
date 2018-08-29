import time
import random

from btrack import track_beats
from lights import (
    Grid, hsv, WHITE,
    Spotlight
)


grid = Grid(interp=True)

spot = Spotlight(grid, 0, 0, 16, 8)
pos = 50


with track_beats() as tracker:
    for f in grid.fps(60):
        pos -= 0.7
        if pos < 0:
            pos += 50

        fade_col = hsv(f / 10)
        grid.darken(tuple(0.90 + 0.08 * (c / 255) for c in fade_col))

        spot.x = round(pos)
        spot.intensity *= 0.95

        if tracker.has_beats():
            intensity = min(tracker.vol, 0.1) / 0.1
            spot.intensity = intensity
        spot.set(WHITE)
        if spot.x > 42:
            spot.x -= 50
            spot.set(WHITE)
