import time
import random
from itertools import count

from btrack import track_beats
from lights import (
    Grid, hsv, RED, CYAN, YELLOW, GREEN, PURPLE, BLUE, WHITE, BLACK,
    Block, Spotlight
)


grid = Grid(interp=False)


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def lcm(a, b):
    return a * b / gcd(a, b)

layout1 = [Block(grid, x, 0, 10, 8) for x in range(0, 50, 10)]
layout2 = (
    [Block(grid, x, 0, 10, 4) for x in range(0, 50, 10)] +
    [Block(grid, x, 4, 10, 4) for x in range(40, -1, -10)]
)
layout3 = [Spotlight(grid, x, 0, 10, 8) for x in range(0, 50, 10)]
layout4 = (
    [Spotlight(grid, x, 0, 8, 4) for x in range(0, 50, 10)] +
    [Spotlight(grid, x, 4, 8, 4) for x in range(36, -1, -10)]
)
layouts = [
    layout1, layout2,
#    layout3, layout4
]

blocks = random.choice(layouts)
random.shuffle(blocks)

colors = [
    RED,
    CYAN,
    YELLOW,
    GREEN,
    PURPLE,
    BLUE,
]


for i, b in enumerate(blocks):
    b.hue = i * 60


TEMPO = 100.0

off = 0

with track_beats() as tracker:
    for f in count():
        if off == 0:
            grid.fill(BLACK)
        off += 1
        for i, b in enumerate(blocks):
            b.set(colors[(i + off) % len(colors)])
        if f % 10 == 0:
            blocks = random.choice(layouts)
            random.shuffle(blocks)
            maxstep = lcm(len(blocks), len(colors))
            off = 0
        while not tracker.has_beats():
            time.sleep(0.01)
        grid.flip()
