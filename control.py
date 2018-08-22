import sys
import subprocess
import atexit
import time

import pygame
from pygame.locals import QUIT, JOYBUTTONDOWN, JOYAXISMOTION, KEYDOWN
from pygame import event
from pygame import joystick

from lights import Grid


pygame.display.init()
joystick.init()
pygame.display.set_mode((1, 1))
grid = Grid(port=7891)
screen = grid.surface()


#if joystick.get_count() < 1:
#    sys.exit('No joysticks detected')


scripts = [
    'rainbow',
    'disco',
    'waves',
    'sparks',
    'flag',
    'hearts',
#    'text',
    'stars',
    'strobe',
]

icons = [
    pygame.image.load('icons/{}.png'.format(s))
    for s in scripts
]

proc = None


def start(script):
    """Start a script."""
    global proc
    if proc:
        proc.terminate()
    proc = subprocess.Popen([sys.executable, '{}.py'.format(script)])


def stop():
    global proc
    if proc:
        proc.terminate()
        proc.wait()
        proc = None


def stop_and_clear():
    stop()
    subprocess.call([sys.executable, 'single_color.py', 'black'])


def stop_and_clear_all():
    stop_and_clear()
    grid.clear()
    grid.flip()


def move(dir):
    """Move the selection, in a given direction."""
    global current, touch
    assert dir in (-1, 1)
    touch = time.time()
    current = (current + dir) % len(scripts)


def activate():
    """Activate the selected script."""
    global touch
    touch = time.time()
    start(scripts[current])


def update():
    global pos
    if time.time() - touch > 5:
        grid.darken()
    else:
        left_icon = icons[int(pos // 8) % len(icons)]
        right_icon = icons[int(pos // 8 + 1) % len(icons)]
        target_pos = current * 8
        pos = pos * 0.6 + target_pos * 0.4

        edge = round((pos // 8 * 8) + 56 - pos)
        screen.blit(left_icon, (edge, 0))
        screen.blit(right_icon, (edge + 8, 0))
        grid.blitsurf(screen)


touch = time.time()
pos = current = 0
atexit.register(stop_and_clear_all)
start(scripts[current])


if joystick.get_count() > 0:
    j = joystick.Joystick(0)
    j.init()
for f in grid.fps(20):
    for ev in event.get():
        if ev.type == QUIT:
            sys.exit(0)
        elif ev.type == JOYAXISMOTION:
            if ev.axis == 0:
                pos = round(ev.value)
                move(dir)
        elif ev.type == JOYBUTTONDOWN:
            if ev.button == 1:
                stop_and_clear()
            elif ev.button == 2:
                activate()
        elif ev.type == KEYDOWN:
            if ev.key == pygame.K_LEFT:
                move(-1)
            elif ev.key == pygame.K_RIGHT:
                move(1)
            elif ev.key == pygame.K_RETURN:
                activate()
            elif ev.key == pygame.K_ESCAPE:
                stop_and_clear()
    update()
