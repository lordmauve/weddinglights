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
    'spots',
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
    global current
    assert dir in (-1, 1)
    current = current + dir


def activate():
    """Activate the selected script."""
    global last_current
    start(scripts[current])
    last_current = current


def update():
    global pos, current
    since_touch = time.time() - touch

    if since_touch > 7:
        current = last_current
        pos = last_current * 8
    elif since_touch > 5:
        grid.darken(0.9)
    else:
        left_icon = icons[int(pos // 8) % len(icons)]
        right_icon = icons[int(pos // 8 + 1) % len(icons)]

        edge = pos // 8 * 8 + 56 - pos
        screen.blit(left_icon, (edge, 0))
        if pos % 8:
            screen.blit(right_icon, (edge + 8, 0))
        grid.blitsurf(screen)

        target_pos = current * 8
        if abs(target_pos - pos) < 0.5:
            pos = target_pos
        else:
            pos = pos * 0.6 + target_pos * 0.4


touch = time.time()
pos = current = last_current = 0
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
            touch = time.time()
            if ev.axis == 0:
                pos = round(ev.value)
                move(dir)
        elif ev.type == JOYBUTTONDOWN:
            touch = time.time()
            if ev.button == 1:
                stop_and_clear()
            elif ev.button == 2:
                activate()
        elif ev.type == KEYDOWN:
            touch = time.time()
            if ev.key == pygame.K_LEFT:
                move(-1)
            elif ev.key == pygame.K_RIGHT:
                move(1)
            elif ev.key == pygame.K_RETURN:
                activate()
            elif ev.key == pygame.K_ESCAPE:
                stop_and_clear()
    update()
