from lights import Grid

from pygame.image import load


heart = load('images/heart.png')

grid = Grid()
screen = grid.surface()


for t in grid.fps(3):
    screen.fill((0, 0, 0))
    for x in range(0, 64, 32):
        screen.blit(heart, ((t + x) % 64, 0))
    grid.blitsurf(screen)
