from lights import Grid, CYAN, BLUE

from itertools import cycle

from pygame import Surface
from pygame import surfarray
from pygame import font


MESSAGES = [
    ("Kathryn & Daniel", (220, 160, 100)),
    ("1st September 2018", (100, 160, 50)),
]


font.init()
f = font.Font('fonts/Vera.ttf', 8)

screen = Surface((64, 8), 0, 24)


messages = cycle(MESSAGES)


def next_message():
    global msg_surf, w, pos
    msg, color = next(messages)
    msg_surf = f.render(msg, True, color)
    w = msg_surf.get_width()
    pos = 64


next_message()

grid = Grid()
for t in grid.fps(20):
    pos -= 1
    screen.fill((0, 0, 0))
    screen.blit(msg_surf, (pos, -1))

    if pos < -w:
        next_message()

    buf = surfarray.array3d(screen)
    buf = buf.transpose([1, 0, 2])[:, ::-1, :]
    grid.pixels = buf.reshape(64 * 8, 3)
