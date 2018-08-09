#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc
import time

from itertools import count

numLEDs = 512
client = opc.Client('localhost:7890')

RED = 255, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
BLACK = 0, 0, 0


COLORS = [RED, WHITE, GREEN, BLACK]

pixels = [RED] * 8 * 64

for t in count():
    for j in range(8):
        for i in range(50):
            pixels[i + j * 64] = COLORS[(i + t) // 4 % len(COLORS)]

    client.put_pixels(pixels)
    time.sleep(0.1)
