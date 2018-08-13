import sys
import pygame
import subprocess
import atexit
from pygame.locals import QUIT, JOYBUTTONDOWN, JOYAXISMOTION
from pygame import event
from pygame import joystick

pygame.display.init()
joystick.init()
#pygame.display.set_mode((1, 1))

if joystick.get_count() < 1:
    sys.exit('No joysticks detected')


scripts = [
    'rainbow',
    'disco',
    'sparks',
    'flag',
    'hearts',
    'text',
    'stars',
]


proc = None

def start(script):
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

atexit.register(stop_and_clear)


current = 0
start(scripts[current])


j = joystick.Joystick(0)
j.init()
while True:
    ev = event.wait()
    if ev.type == QUIT:
        sys.exit(0)
    elif ev.type == JOYAXISMOTION:
        if ev.axis == 0:
            pos = round(ev.value)
            current = (current + pos) % len(scripts)
            start(scripts[current])
    elif ev.type == JOYBUTTONDOWN:
        if ev.button == 1:
            stop_and_clear()
        elif ev.button == 2:
            start(scripts[current])
