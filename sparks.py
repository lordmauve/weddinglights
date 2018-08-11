"""Fire a shower of pink sparks down the grid.

Each spark has an intensity which affects its color and its speed.

"""
import time
from itertools import count
from collections import namedtuple
from operator import attrgetter
import random


from lights import Grid


PINK = 255, 80, 128


grid = Grid()


Spark = namedtuple('Spark', 'x y color vx intensity')


def run_sparks():
    sparks = []

    for t in grid.fps(60):
        sparks.sort(key=attrgetter('intensity'))
        newsparks = []
        grid.darken(0.8)
        for s in sparks:
            s = s._replace(
                x=s.x + s.vx
            )
            x = round(s.x)
            if 0 <= x < grid.W:
                grid[x, s.y] = s.color
                newsparks.append(s)
            elif x < 0:
                newsparks.append(s)
        sparks = newsparks

        if random.random() > 0.7:
            intensity = random.random() ** 2
            if intensity < 0.5:
                color = tuple(round(c * (intensity ** 1.2 * 1.5 + 0.25)) for c in PINK)
            else:
                i = (1.0 - (intensity * 2.0 - 1.0) * 0.7)
                color = tuple(round(255 - (255 - c) * i) for c in PINK)

            sparks.append(Spark(
                x=-random.random(),
                y=grid.rand_y(),
                color=color,
                vx=intensity ** 1.5 * 0.5 + 0.05,
                intensity=intensity,
            ))


if __name__ == '__main__':
    run_sparks()
