from colors import BLACK
import random
import time

import opc

client = opc.Client('localhost:7890')


class Grid:
    W = 50
    H = 8

    def __init__(self, interp=True):
        self.pixels = [BLACK] * 8 * 64
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
        client.put_pixels(self.pixels)

    def rand_x(self):
        return random.randrange(self.W)

    def rand_y(self):
        return random.randrange(self.H)

    def rand_pos(self):
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
