import time
import random

from lights import Grid, hsv, RED, CYAN, YELLOW, GREEN, PURPLE, BLUE, WHITE


grid = Grid(interp=False)


class Block:
    def __init__(self, grid, x, y, w, h):
        self.grid = grid
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def set(self, color):
        for j in range(self.y, self.y + self.h):
            for i in range(self.x, self.x + self.w):
                self.grid[i, j] = color


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
layouts = [layout1, layout2]

blocks = random.choice(layouts)

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

maxstep = lcm(len(blocks), len(colors))
for f in grid.fps(TEMPO / 60.0):
    off += random.randrange(1, maxstep)
    for i, b in enumerate(blocks):
        b.set(colors[(i + off) % len(colors)])
    if f % 10 == 0:
        blocks = random.choice(layouts)
        maxstep = lcm(len(blocks), len(colors))
