import random
import time
import os

from .colors import BLACK
from . import opc

CLIENT_HOST = os.environ.get('OPC_HOST', 'localhost')
client = opc.Client(CLIENT_HOST + ':7890')


class Grid:
    W = 50
    H = 8

    def __init__(self, interp=True):
        self.pixels = self.last_pixels = [BLACK] * 8 * 64
        client.set_interpolation(interp)

    def __setitem__(self, p, color):
        x, y = p
        if len(color) != 3:
            raise TypeError("Invalid color value: {!r}".format(color))
        if 0 <= x < self.W and 0 <= y < self.H:
            self.pixels[x + y * 64] = color
        else:
            raise IndexError("Index out of bounds: {!r}".format(p))

    def __getitem__(self, p):
        x, y = p
        if 0 <= x < self.W and 0 <= y < self.H:
            return self.pixels[x + y * 64]
        else:
            raise IndexError("Index out of bounds: {!r}".format(p))

    def keys(self):
        for y in range(self.H):
            for x in range(self.W):
                yield x, y

    def items(self):
        for y in range(self.H):
            for x in range(self.W):
                yield (x, y), self.pixels[x + y * 64]

    def flip(self):
        self.last_pixels = self.pixels[:]
        client.put_pixels(self.pixels)

    def fill(self, color):
        """Fill the grid with a single color."""
        self.pixels = [color] * len(self.pixels)

    def clear(self):
        """Clear the whole grid (set it to black)."""
        self.pixels = [BLACK] * len(self.pixels)

    def fade(self, duration=1.0):
        t = 0
        DELAY = 0.02
        values = self.last_pixels[:]

        while t < duration:
            frac = t / duration
            for y in range(self.H):
                for x in range(self.W):
                    idx = x + y * 64
                    a = self.last_pixels[idx]
                    b = self.pixels[idx]
                    values[idx] = tuple(
                        frac * b[c] + (1 - frac) * a[c]
                        for c in range(3)
                    )

            client.put_pixels(values)
            time.sleep(DELAY)
            t += DELAY
        self.flip()

    def darken(self, factor=0.6):
        """Darken all pixels on the grid by a multiple."""
        if not (0 <= factor <= 1):
            raise ValueError('Cannot darken by factor of {}'.format(factor))

        factor = round(255 * factor)
        for y in range(self.H):
            for x in range(self.W):
                idx = x + y * 64
                v = self.pixels[idx]
                self.pixels[idx] = tuple((c * factor) // 255 for c in v)

    def rand_x(self):
        """Return a random position in the x axis."""
        return random.randrange(self.W)

    def rand_y(self):
        """Return a random position in the y axis."""
        return random.randrange(self.H)

    def rand_pos(self):
        """Return a random position in the grid."""
        return (
            random.randrange(self.W),
            random.randrange(self.H)
        )

    def fps(self, rate):
        delay = 1.0 / rate
        frame = 0
        while True:
            yield frame
            frame += 1
            client.put_pixels(self.pixels)
            time.sleep(delay)
