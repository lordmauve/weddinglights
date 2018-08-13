import time
from lights import Grid

from itertools import count

from pygame import Surface
from pygame.image import load
from pygame import surfarray


heart = load('heart.png')

screen = Surface((64, 8), 0, 24)


grid = Grid()
for t in grid.fps(3):
    screen.fill((0, 0, 0))
    for x in range(0, 64, 13):
        screen.blit(heart, ((t + x) % 64, 0))
    buf = surfarray.array3d(screen)
    buf = buf.transpose([1, 0, 2])[:,::-1,:]
    grid.pixels = buf.reshape(64 * 8, 3)
